import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Zap, TrendingUp, TrendingDown, Minus, RefreshCw, Info } from 'lucide-react'
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend,
  ReferenceLine,
} from 'recharts'
import PageTransition from '../components/PageTransition'
import { forecastAPI } from '../lib/api'

const trendIcon = {
  rising:  { icon: TrendingUp,   color: 'text-green-600 dark:text-green-400', bg: 'bg-green-100 dark:bg-green-900/30', label: 'Rising' },
  falling: { icon: TrendingDown, color: 'text-red-600 dark:text-red-400',     bg: 'bg-red-100 dark:bg-red-900/30',     label: 'Falling' },
  stable:  { icon: Minus,        color: 'text-amber-600 dark:text-amber-400', bg: 'bg-amber-100 dark:bg-amber-900/30', label: 'Stable' },
}

export default function Forecast() {
  const [forecasts, setForecasts] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const d = await forecastAPI.top(8, 90)
      setForecasts(d.forecasts || [])
      if (d.forecasts?.length) setSelected(d.forecasts[0])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-wrap justify-between items-start gap-4">
          <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}>
            <span className="badge-brand mb-3 inline-flex"><Zap size={12} className="mr-1"/> Powered by Facebook Prophet</span>
            <h1 className="font-display text-3xl sm:text-4xl font-bold">Skill Demand Forecast</h1>
            <p className="mt-2 text-ink-600 dark:text-ink-400 max-w-2xl">
              90-day predictions based on time-series analysis. Plan your learning path based on where the market is heading, not just where it is.
            </p>
          </motion.div>
          <button onClick={load} className="btn-secondary">
            <RefreshCw size={14}/> Refresh
          </button>
        </div>

        {loading ? (
          <div className="card p-12 mt-8 shimmer h-96"></div>
        ) : forecasts.length === 0 ? (
          <div className="card p-12 text-center mt-8">
            <p className="text-ink-500">No forecasts available. Try refreshing.</p>
          </div>
        ) : (
          <>
            {/* Skill picker - horizontal scrolling pill bar */}
            <div className="mt-8 -mx-2 px-2 overflow-x-auto pb-2">
              <div className="flex gap-2 min-w-min">
                {forecasts.map((f) => {
                  const T = trendIcon[f.trend] || trendIcon.stable
                  const isActive = selected?.skill === f.skill
                  return (
                    <button
                      key={f.skill}
                      onClick={() => setSelected(f)}
                      className={`flex-shrink-0 px-4 py-2.5 rounded-lg border-2 transition-all flex items-center gap-2 whitespace-nowrap ${
                        isActive
                          ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/30 shadow-md shadow-brand-500/10'
                          : 'border-ink-200 dark:border-ink-800 hover:border-brand-400 bg-white dark:bg-ink-900'
                      }`}
                    >
                      <T.icon className={T.color} size={16}/>
                      <span className={`font-medium text-sm ${isActive ? 'text-brand-700 dark:text-brand-300' : ''}`}>{f.skill}</span>
                      <span className={`text-xs ${T.color} opacity-70`}>· {T.label}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Selected forecast detail */}
            <AnimatePresence mode="wait">
              {selected && <ForecastChart key={selected.skill} forecast={selected}/>}
            </AnimatePresence>

            {/* Trend summary cards */}
            <div className="grid md:grid-cols-3 gap-3 mt-6">
              <TrendSummary
                title="Rising"
                forecasts={forecasts.filter(f => f.trend === 'rising')}
                colorClass="text-green-600 dark:text-green-400"
                bgClass="bg-green-50 dark:bg-green-900/10 border-green-200 dark:border-green-900/30"
                Icon={TrendingUp}
                onClick={setSelected}
              />
              <TrendSummary
                title="Stable"
                forecasts={forecasts.filter(f => f.trend === 'stable')}
                colorClass="text-amber-600 dark:text-amber-400"
                bgClass="bg-amber-50 dark:bg-amber-900/10 border-amber-200 dark:border-amber-900/30"
                Icon={Minus}
                onClick={setSelected}
              />
              <TrendSummary
                title="Falling"
                forecasts={forecasts.filter(f => f.trend === 'falling')}
                colorClass="text-red-600 dark:text-red-400"
                bgClass="bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-900/30"
                Icon={TrendingDown}
                onClick={setSelected}
              />
            </div>
          </>
        )}
      </div>
    </PageTransition>
  )
}

function ForecastChart({ forecast }) {
  // Combine history + forecast for the chart
  const combined = [
    ...forecast.history.map(h => ({ date: h.date, historical: h.demand })),
    ...forecast.forecast.map(f => ({
      date: f.date,
      predicted: f.predicted,
      lower: f.lower,
      upper: f.upper,
    })),
  ]

  const T = trendIcon[forecast.trend] || trendIcon.stable
  const historyEnd = forecast.history[forecast.history.length - 1]?.date
  const recentDemand = forecast.history.slice(-7).reduce((s, h) => s + h.demand, 0) / 7
  const futureDemand = forecast.forecast.slice(0, 30).reduce((s, f) => s + f.predicted, 0) / 30
  const change = recentDemand > 0 ? ((futureDemand - recentDemand) / recentDemand * 100).toFixed(1) : 0

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="card p-6 mt-4"
    >
      <div className="flex flex-wrap items-start justify-between gap-3 mb-5">
        <div>
          <h3 className="font-display text-2xl font-bold flex items-center gap-2">
            {forecast.skill}
            <span className={`badge ${T.bg} ${T.color} text-xs`}>
              <T.icon size={11} className="mr-1"/> {T.label}
            </span>
          </h3>
          <p className="text-sm text-ink-500 mt-1">
            {forecast.history.length} days of history · {forecast.forecast.length} days forecast
          </p>
        </div>
        <div className={`text-right ${T.color}`}>
          <div className="text-2xl font-bold">
            {change > 0 ? '+' : ''}{change}%
          </div>
          <div className="text-xs text-ink-500">expected change (30d)</div>
        </div>
      </div>

      <ResponsiveContainer width="100%" height={360}>
        <AreaChart data={combined} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
          <defs>
            <linearGradient id="histGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.5}/>
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="forecastGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.5}/>
              <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
            </linearGradient>
            <linearGradient id="confGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.18}/>
              <stop offset="95%" stopColor="#f59e0b" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
          <XAxis dataKey="date" stroke="currentColor" opacity={0.5} fontSize={11} tickFormatter={(d) => d?.slice(5)}/>
          <YAxis stroke="currentColor" opacity={0.5} fontSize={11}/>
          <Tooltip
            contentStyle={{ background: 'rgba(15,23,42,0.95)', border: 'none', borderRadius: 8, color: 'white' }}
            labelStyle={{ color: '#c7d2fe' }}
          />
          <Legend wrapperStyle={{ fontSize: 12 }}/>
          {historyEnd && (
            <ReferenceLine x={historyEnd} stroke="#94a3b8" strokeDasharray="4 4" label={{ value: 'Today', position: 'top', fontSize: 10, fill: '#94a3b8' }}/>
          )}
          <Area type="monotone" dataKey="upper" stroke="none" fill="url(#confGrad)" name="Upper bound"/>
          <Area type="monotone" dataKey="historical" stroke="#6366f1" strokeWidth={2.5} fill="url(#histGrad)" name="Historical"/>
          <Area type="monotone" dataKey="predicted" stroke="#f59e0b" strokeWidth={2.5} strokeDasharray="5 5" fill="url(#forecastGrad)" name="Forecast"/>
        </AreaChart>
      </ResponsiveContainer>

      <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-sm">
        <Stat label="Recent demand" value={Math.round(recentDemand)} unit="/day"/>
        <Stat label="Forecast (30d)" value={Math.round(futureDemand)} unit="/day"/>
        <Stat label="History points" value={forecast.history.length}/>
        <Stat label="Trend" value={T.label} valueClass={T.color}/>
      </div>

      {forecast.is_synthetic && (
        <div className="mt-4 flex items-start gap-2 p-3 rounded-lg bg-ink-100 dark:bg-ink-800/50 text-xs text-ink-600 dark:text-ink-400">
          <Info size={14} className="flex-shrink-0 mt-0.5"/>
          <span>
            Historical baseline is modeled from observed frequency plus standard weekly hiring patterns.
            Real day-by-day history will replace this baseline as new jobs are ingested over time.
          </span>
        </div>
      )}
    </motion.div>
  )
}

function Stat({ label, value, unit = '', valueClass = '' }) {
  return (
    <div className="p-3 rounded-lg bg-ink-50 dark:bg-ink-800/60">
      <div className="text-ink-500 text-xs">{label}</div>
      <div className={`font-bold text-lg ${valueClass}`}>
        {value}{unit && <span className="text-xs font-normal text-ink-500 ml-0.5">{unit}</span>}
      </div>
    </div>
  )
}

function TrendSummary({ title, forecasts, colorClass, bgClass, Icon, onClick }) {
  return (
    <div className={`rounded-xl border p-5 ${bgClass}`}>
      <div className="flex items-center gap-2 mb-3">
        <Icon size={16} className={colorClass}/>
        <span className={`font-semibold ${colorClass}`}>{title}</span>
        <span className="text-xs text-ink-500 ml-auto">{forecasts.length} skills</span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        {forecasts.length === 0 ? (
          <span className="text-xs text-ink-500">No skills in this category</span>
        ) : (
          forecasts.map(f => (
            <button
              key={f.skill}
              onClick={() => onClick(f)}
              className="text-xs px-2 py-1 rounded-md bg-white dark:bg-ink-900 border border-ink-200 dark:border-ink-700 hover:border-brand-500 transition-colors"
            >
              {f.skill}
            </button>
          ))
        )}
      </div>
    </div>
  )
}
