import { useState } from 'react'
import { motion } from 'framer-motion'
import { MapPin, Building2, ExternalLink, Bookmark, Clock, Wifi } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuth } from '../context/AuthContext'
import { userAPI } from '../lib/api'

const sourceColors = {
  adzuna:   'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
  remotive: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
  jsearch:  'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  jooble:   'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
}

const sourceLabel = {
  adzuna:   'Adzuna',
  remotive: 'Remotive',
  jsearch:  'LinkedIn/Indeed',
  jooble:   'Jooble',
}

/**
 * Try to extract a domain from the company name for fetching its logo.
 * Falls back to a generated avatar if no domain can be guessed.
 */
function getCompanyLogoUrl(company) {
  if (!company) return null
  // try common cases - cleanup whitespace and try .com
  const slug = company
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[^a-z0-9]/g, '')
    .replace(/(inc|llc|ltd|pvt|technologies|technology|solutions|systems|services|corp|corporation|company|co|incorporated|limited)$/g, '')
  if (!slug || slug.length < 2) return null
  // logo.dev offers a free logo lookup by domain (publicly available, no auth required)
  return `https://img.logo.dev/${slug}.com?token=pk_X-1ZO13GSgeOoUrIuJ6GMQ&size=80&format=png`
}

export default function JobCard({ job, index = 0 }) {
  const { user, isAuthenticated } = useAuth()
  const [logoError, setLogoError] = useState(false)
  const [saved, setSaved] = useState(false)

  const handleSave = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (!isAuthenticated) {
      toast.error('Please sign in to save jobs')
      return
    }
    try {
      await userAPI.save(user.user_id, { job_id: job.job_id })
      setSaved(true)
      toast.success('Saved!')
    } catch (err) {
      toast.error('Could not save job')
    }
  }

  const skills = (job.extracted_skills || []).slice(0, 6)
  const moreSkills = (job.extracted_skills || []).length - 6
  const logoUrl = getCompanyLogoUrl(job.company)
  const initials = (job.company || '?').split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase()

  const postedAgo = (() => {
    if (!job.posted_date) return null
    const diff = Date.now() - new Date(job.posted_date).getTime()
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))
    if (days < 1) return 'today'
    if (days === 1) return 'yesterday'
    if (days < 7) return `${days}d ago`
    if (days < 30) return `${Math.floor(days / 7)}w ago`
    return `${Math.floor(days / 30)}mo ago`
  })()

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.04, 0.5), duration: 0.4 }}
      whileHover={{ y: -4 }}
      className="card p-5 group hover-glow flex flex-col"
    >
      {/* Header: logo + source badge */}
      <div className="flex items-start gap-3 mb-3">
        <div className="flex-shrink-0 w-11 h-11 rounded-xl overflow-hidden bg-gradient-to-br from-brand-100 to-brand-200 dark:from-brand-900/40 dark:to-brand-800/40 flex items-center justify-center font-bold text-brand-700 dark:text-brand-300 ring-1 ring-brand-500/10">
          {logoUrl && !logoError ? (
            <img
              src={logoUrl}
              alt={job.company}
              className="w-full h-full object-contain p-1"
              onError={() => setLogoError(true)}
              loading="lazy"
            />
          ) : (
            <span>{initials}</span>
          )}
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="font-semibold text-base leading-snug line-clamp-2 group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">
            {job.title}
          </h3>
          <p className="text-sm text-ink-600 dark:text-ink-400 truncate mt-0.5">
            {job.company}
          </p>
        </div>
        {job.source && (
          <span className={`badge ${sourceColors[job.source] || 'bg-ink-200 text-ink-700'} text-xs flex-shrink-0`}>
            {sourceLabel[job.source] || job.source}
          </span>
        )}
      </div>

      {/* Meta row */}
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-500">
        {job.location && (
          <span className="flex items-center gap-1"><MapPin size={11}/> {job.location}</span>
        )}
        {job.is_remote && (
          <span className="flex items-center gap-1 text-green-600 dark:text-green-400">
            <Wifi size={11}/> Remote
          </span>
        )}
        {postedAgo && (
          <span className="flex items-center gap-1"><Clock size={11}/> {postedAgo}</span>
        )}
      </div>

      {/* Skills */}
      {skills.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {skills.map(s => (
            <span key={s} className="badge-brand text-xs">{s}</span>
          ))}
          {moreSkills > 0 && (
            <span className="badge text-xs text-ink-500 bg-ink-100 dark:bg-ink-800">+{moreSkills}</span>
          )}
        </div>
      )}

      {/* Salary */}
      {(job.salary_min || job.salary_max) ? (
        <div className="mt-3 text-sm font-semibold text-green-600 dark:text-green-400">
          {job.salary_currency || ''} {(job.salary_min || 0).toLocaleString()} - {(job.salary_max || 0).toLocaleString()}
        </div>
      ) : null}

      {/* Actions */}
      <div className="mt-4 flex items-center gap-2 pt-3 border-t border-ink-100 dark:border-ink-800 mt-auto">
        <a
          href={job.source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="btn-primary text-sm flex-1 justify-center text-xs sm:text-sm"
        >
          View & Apply <ExternalLink size={13}/>
        </a>
        <button
          onClick={handleSave}
          className={`btn-secondary text-sm ${saved ? '!text-amber-600 !border-amber-500/50' : ''}`}
          title="Save job"
        >
          <Bookmark size={14} className={saved ? 'fill-current' : ''}/>
        </button>
      </div>
    </motion.div>
  )
}
