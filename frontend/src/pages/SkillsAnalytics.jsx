import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Sparkles, BarChart3, PieChart as PieIcon, Award, ArrowUpRight, ArrowDownRight } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  PieChart, Pie, Legend, CartesianGrid,
} from 'recharts'
import PageTransition from '../components/PageTransition'
import { SkeletonBar } from '../components/Skeleton'
import { skillsAPI } from '../lib/api'

const palette = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#f59e0b', '#fbbf24', '#10b981', '#14b8a6', '#06b6d4', '#3b82f6', '#ec4899', '#f43f5e']

export default function SkillsAnalytics() {
  const [tab, setTab] = useState('top')
  const [top, setTop] = useState([])
  const [trending, setTrending] = useState([])
  const [emerging, setEmerging] = useState([])
  const [declining, setDeclining] = useState([])
  const [categories, setCategories] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      skillsAPI.top(15),
      skillsAPI.trending(10),
      skillsAPI.emerging(10),
      skillsAPI.declining(10),
      skillsAPI.categories(),
    ])
    .then(([t, tr, em, dec, cat]) => {
      setTop(t.results || [])
      setTrending(tr.results || [])
      setEmerging(em.results || [])
      setDeclining(dec.results || [])
      setCategories(cat.distribution || {})
    })
    .catch(() => {})
    .finally(() => setLoading(false))
  }, [])

  const categoryData = Object.entries(categories).map(([name, value]) => ({ name, value })).slice(0, 10)

  const tabs = [
    { id: 'top',       label: 'Top Skills',     icon: Award },
    { id: 'trending',  label: 'Trending',       icon: TrendingUp },
    { id: 'emerging',  label: 'Emerging',       icon: Sparkles },
    { id: 'declining', label: 'Declining',      icon: TrendingDown },
    { id: 'categories',label: 'Categories',     icon: PieIcon },
  ]

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{opacity:0,y:10}} animate={{opacity:1,y:0}}>
          <h1 className="font-display text-3xl sm:text-4xl font-bold">Skills Analytics</h1>
          <p className="mt-2 text-ink-600 dark:text-ink-400">
            Data-driven insights from thousands of job postings across India and globally.
          </p>
        </motion.div>

        {/* Tabs */}
        <div className="mt-6 flex flex-wrap gap-2">
          {tabs.map(t => (
            <button
              key={t.id}
              onClick={() => setTab(t.id)}
              className={`px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-all ${
                tab === t.id
                  ? 'bg-brand-600 text-white shadow-md shadow-brand-600/20'
                  : 'bg-ink-100 dark:bg-ink-800 text-ink-600 dark:text-ink-400 hover:bg-ink-200 dark:hover:bg-ink-700'
              }`}
            >
              <t.icon size={15}/> {t.label}
            </button>
          ))}
        </div>

        <div className="mt-6">
          {loading ? (
            <div className="card p-6 space-y-3">
              {Array.from({length: 8}).map((_, i) => (
                <div key={i} className="flex gap-3 items-center">
                  <SkeletonBar width="w-32" />
                  <SkeletonBar height="h-3" />
                </div>
              ))}
            </div>
          ) : tab === 'top' ? (
            <TopSkillsView data={top} />
          ) : tab === 'trending' ? (
            <GrowthView data={trending} positive title="Trending Skills" subtitle="Skills with highest growth in recent job postings" />
          ) : tab === 'emerging' ? (
            <GrowthView data={emerging} positive title="Emerging Skills" subtitle="Brand new skills appearing on the radar" />
          ) : tab === 'declining' ? (
            <GrowthView data={declining} positive={false} title="Declining Skills" subtitle="Skills losing demand in recent weeks" />
          ) : (
            <CategoryView data={categoryData} />
          )}
        </div>
      </div>
    </PageTransition>
  )
}

function TopSkillsView({ data }) {
  if (!data.length) return <EmptyState />
  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <div className="card p-6 lg:col-span-2">
        <h3 className="font-semibold mb-4 flex items-center gap-2"><BarChart3 size={18}/> Most In-Demand Skills</h3>
        <ResponsiveContainer width="100%" height={420}>
          <BarChart data={data} layout="vertical" margin={{ left: 80, right: 30 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1} />
            <XAxis type="number" stroke="currentColor" opacity={0.5} fontSize={12}/>
            <YAxis dataKey="skill" type="category" stroke="currentColor" opacity={0.7} fontSize={12} width={75}/>
            <Tooltip
              contentStyle={{ background: 'rgba(15,23,42,0.95)', border: 'none', borderRadius: 8, color: 'white' }}
              cursor={{ fill: 'rgba(99,102,241,0.1)' }}
            />
            <Bar dataKey="count" radius={[0, 6, 6, 0]}>
              {data.map((_, i) => <Cell key={i} fill={palette[i % palette.length]} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="card p-6">
        <h3 className="font-semibold mb-4">Top 10 List</h3>
        <ol className="space-y-2.5">
          {data.slice(0, 10).map((s, i) => (
            <li key={s.skill} className="flex items-center gap-3">
              <span className="w-7 h-7 rounded-lg bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 flex items-center justify-center text-xs font-bold flex-shrink-0">{i + 1}</span>
              <div className="min-w-0 flex-1">
                <div className="font-medium truncate">{s.skill}</div>
                <div className="text-xs text-ink-500">{s.count} jobs · {s.percentage}%</div>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </div>
  )
}

function GrowthView({ data, positive, title, subtitle }) {
  if (!data.length) return <EmptyState />
  return (
    <div className="card p-6">
      <h3 className="font-semibold mb-1">{title}</h3>
      <p className="text-sm text-ink-500 mb-5">{subtitle}</p>
      <div className="space-y-2">
        {data.map((s, i) => (
          <motion.div
            key={s.skill}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.04 }}
            className="flex items-center gap-4 p-3 rounded-lg hover:bg-ink-50 dark:hover:bg-ink-800/50 transition-colors"
          >
            <span className="w-8 text-ink-400 text-sm">#{i + 1}</span>
            <div className="flex-1 min-w-0">
              <div className="font-medium">{s.skill}</div>
              <div className="text-xs text-ink-500">
                {s.recent_count} recent vs {s.previous_count} previous
              </div>
            </div>
            <div className={`flex items-center gap-1 font-bold text-sm ${positive ? 'text-green-600' : 'text-red-600'}`}>
              {positive ? <ArrowUpRight size={16}/> : <ArrowDownRight size={16}/>}
              {s.growth_rate > 500 ? 'NEW' : `${s.growth_rate > 0 ? '+' : ''}${s.growth_rate}%`}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

function CategoryView({ data }) {
  if (!data.length) return <EmptyState />
  return (
    <div className="grid lg:grid-cols-2 gap-6">
      <div className="card p-6">
        <h3 className="font-semibold mb-4">Distribution by Skill Category</h3>
        <ResponsiveContainer width="100%" height={400}>
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" outerRadius={140} label={(e) => e.name}>
              {data.map((_, i) => <Cell key={i} fill={palette[i % palette.length]} />)}
            </Pie>
            <Tooltip contentStyle={{ background: 'rgba(15,23,42,0.95)', border: 'none', borderRadius: 8, color: 'white' }}/>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="card p-6">
        <h3 className="font-semibold mb-4">Category Breakdown</h3>
        <div className="space-y-3">
          {data.map((c, i) => (
            <div key={c.name}>
              <div className="flex justify-between text-sm mb-1">
                <span className="font-medium">{c.name}</span>
                <span className="text-ink-500">{c.value} jobs</span>
              </div>
              <div className="h-2 bg-ink-100 dark:bg-ink-800 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(c.value / data[0].value) * 100}%` }}
                  transition={{ duration: 0.8, delay: i * 0.05 }}
                  className="h-full rounded-full"
                  style={{ background: palette[i % palette.length] }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function EmptyState() {
  return (
    <div className="card p-12 text-center">
      <p className="text-ink-500">No data yet. Run the data ingestion endpoint or search some jobs first.</p>
      <p className="text-xs text-ink-400 mt-2">
        Tip: POST to <code className="px-2 py-0.5 rounded bg-ink-100 dark:bg-ink-800">/api/jobs/ingest</code> to populate the database.
      </p>
    </div>
  )
}
