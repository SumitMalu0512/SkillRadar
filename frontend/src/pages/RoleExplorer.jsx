import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { RefreshCw, Layers, Sparkles, ChevronRight, BarChart3, Briefcase } from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid,
} from 'recharts'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'
import PageTransition from '../components/PageTransition'
import { clustersAPI } from '../lib/api'

const palette = ['#6366f1', '#8b5cf6', '#a78bfa', '#f59e0b', '#10b981', '#06b6d4', '#ec4899', '#f43f5e']

export default function RoleExplorer() {
  const navigate = useNavigate()
  const [clusters, setClusters] = useState([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [selectedId, setSelectedId] = useState(null)

  const load = async () => {
    setLoading(true)
    try {
      const data = await clustersAPI.list()
      setClusters(data.clusters || [])
      // pick the first cluster by default
      if ((data.clusters || []).length > 0 && selectedId === null) {
        setSelectedId(data.clusters[0].cluster_id)
      }
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const refresh = async () => {
    setRefreshing(true)
    try {
      const data = await clustersAPI.refresh(6)
      setClusters(data.summary || [])
      if (data.summary?.length > 0) setSelectedId(data.summary[0].cluster_id)
      toast.success(`Clustering refreshed (Silhouette: ${data.result?.silhouette_score})`)
    } catch (err) {
      toast.error('Need more job data to cluster. Try ingesting jobs first.')
    } finally {
      setRefreshing(false)
    }
  }

  const selected = clusters.find(c => c.cluster_id === selectedId)

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-wrap justify-between items-start gap-4">
          <div>
            <h1 className="font-display text-3xl sm:text-4xl font-bold">Role Clusters</h1>
            <p className="mt-2 text-ink-600 dark:text-ink-400 max-w-2xl">
              K-Means clustering groups similar job roles based on skill requirements,
              revealing natural career paths in the market.
            </p>
          </div>
          <button onClick={refresh} disabled={refreshing} className="btn-secondary">
            <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''}/>
            {refreshing ? 'Clustering...' : 'Refresh Clusters'}
          </button>
        </div>

        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5 mt-8">
            {Array.from({length: 6}).map((_, i) => (
              <div key={i} className="card p-6 h-48 shimmer"></div>
            ))}
          </div>
        ) : clusters.length === 0 ? (
          <div className="card p-12 text-center mt-8">
            <Layers className="mx-auto text-ink-300 mb-3" size={40}/>
            <p className="text-ink-500">No clusters yet. Click "Refresh Clusters" to generate them.</p>
            <p className="text-xs text-ink-400 mt-2">Requires at least 16 jobs with extracted skills in the database.</p>
          </div>
        ) : (
          <div className="grid lg:grid-cols-[1fr,1.4fr] gap-6 mt-8">
            {/* Cluster Cards List - Left */}
            <div className="space-y-3">
              {clusters.map((c, i) => {
                const isActive = c.cluster_id === selectedId
                const color = palette[i % palette.length]
                return (
                  <motion.button
                    key={c.cluster_id}
                    onClick={() => setSelectedId(c.cluster_id)}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className={`w-full text-left card p-5 transition-all group ${
                      isActive
                        ? 'border-brand-500 shadow-lg shadow-brand-500/10 ring-2 ring-brand-500/30'
                        : 'hover:border-brand-400'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className="flex-shrink-0 w-10 h-10 rounded-lg text-white flex items-center justify-center font-bold text-sm"
                        style={{ background: `linear-gradient(135deg, ${color}, ${color}dd)` }}
                      >
                        {c.cluster_id + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h3 className={`font-semibold transition-colors ${
                          isActive ? 'text-brand-600 dark:text-brand-400' : 'group-hover:text-brand-600'
                        }`}>
                          {c.label}
                        </h3>
                        <div className="mt-1 flex items-center gap-3 text-xs text-ink-500">
                          <span className="flex items-center gap-1"><Briefcase size={11}/> {c.job_count} jobs</span>
                          <span>{(c.top_skills || []).length} skills</span>
                        </div>
                      </div>
                      <ChevronRight
                        size={18}
                        className={`transition-all ${
                          isActive ? 'text-brand-500 translate-x-1' : 'text-ink-300 group-hover:text-brand-500'
                        }`}
                      />
                    </div>
                  </motion.button>
                )
              })}
            </div>

            {/* Detail Panel - Right */}
            <AnimatePresence mode="wait">
              {selected && (
                <motion.div
                  key={selected.cluster_id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  {/* Header card */}
                  <div className="card p-6 relative overflow-hidden">
                    <div
                      className="absolute inset-x-0 top-0 h-1"
                      style={{ background: `linear-gradient(90deg, ${palette[selected.cluster_id % palette.length]}, transparent)` }}
                    />
                    <span className="badge-brand inline-flex">
                      <Sparkles size={11} className="mr-1"/> Cluster {selected.cluster_id + 1} of {clusters.length}
                    </span>
                    <h2 className="text-2xl font-display font-bold mt-3">{selected.label}</h2>
                    <p className="text-sm text-ink-600 dark:text-ink-400 mt-1">
                      {selected.job_count} matching jobs · {(selected.top_skills || []).length} key skills identified
                    </p>
                  </div>

                  {/* Skills bar chart */}
                  <div className="card p-6">
                    <h3 className="font-semibold mb-4 flex items-center gap-2">
                      <BarChart3 size={16} className="text-brand-600"/>
                      Top Skills in This Cluster
                    </h3>
                    {(selected.top_skills || []).length > 0 ? (
                      <ResponsiveContainer width="100%" height={Math.max(220, (selected.top_skills.length) * 32)}>
                        <BarChart
                          data={selected.top_skills}
                          layout="vertical"
                          margin={{ left: 90, right: 20 }}
                        >
                          <CartesianGrid strokeDasharray="3 3" stroke="currentColor" opacity={0.1}/>
                          <XAxis type="number" stroke="currentColor" opacity={0.5} fontSize={11}/>
                          <YAxis
                            dataKey="skill"
                            type="category"
                            stroke="currentColor"
                            opacity={0.7}
                            fontSize={12}
                            width={85}
                          />
                          <Tooltip
                            contentStyle={{ background: 'rgba(15,23,42,0.95)', border: 'none', borderRadius: 8, color: 'white' }}
                            cursor={{ fill: 'rgba(99,102,241,0.1)' }}
                          />
                          <Bar dataKey="count" radius={[0, 6, 6, 0]}>
                            {selected.top_skills.map((_, i) => (
                              <Cell key={i} fill={palette[(selected.cluster_id + i) % palette.length]}/>
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    ) : (
                      <p className="text-ink-500 text-sm">No skill data available for this cluster.</p>
                    )}
                  </div>

                  {/* Skill list with action */}
                  <div className="card p-6">
                    <h3 className="font-semibold mb-3">All Skills</h3>
                    <div className="flex flex-wrap gap-1.5 mb-4">
                      {(selected.top_skills || []).map((s) => (
                        <button
                          key={s.skill}
                          onClick={() => navigate(`/jobs?skill=${encodeURIComponent(s.skill)}`)}
                          className="badge-brand text-xs hover:scale-105 transition-transform cursor-pointer"
                          title="Click to find jobs requiring this skill"
                        >
                          {s.skill}
                        </button>
                      ))}
                    </div>
                    <button
                      onClick={() => navigate(`/jobs?q=${encodeURIComponent(selected.label.split(' · ')[0])}`)}
                      className="btn-primary w-full justify-center"
                    >
                      Browse Jobs in This Cluster <ChevronRight size={14}/>
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        )}
      </div>
    </PageTransition>
  )
}
