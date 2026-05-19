import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { MapPin, Wifi, RefreshCw, Globe, Filter, Search } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import PageTransition from '../components/PageTransition'
import JobCard from '../components/JobCard'
import SearchAutocomplete from '../components/SearchAutocomplete'
import { SkeletonGrid } from '../components/Skeleton'
import { jobsAPI } from '../lib/api'

export default function JobSearch() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [query, setQuery] = useState(searchParams.get('q') || searchParams.get('skill') || '')
  const [location, setLocation] = useState(searchParams.get('location') || 'India')
  const [remote, setRemote] = useState(false)
  const [globalSearch, setGlobalSearch] = useState(false)
  const [results, setResults] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  useEffect(() => {
    if (searchParams.get('q') || searchParams.get('skill')) {
      runSearch(searchParams.get('q') || searchParams.get('skill'))
    }
  }, [])

  const runSearch = async (qOverride = null) => {
    const q = (qOverride ?? query)?.trim()
    setLoading(true)
    setHasSearched(true)

    const params = {
      q: q || '',
      location: globalSearch ? 'Worldwide' : location,
      remote: remote || globalSearch,
      limit: 200,
    }
    setSearchParams({ q: params.q, ...(globalSearch ? {} : { location: params.location }) })

    try {
      const data = await jobsAPI.search(params)
      setResults(data.results || [])
      setStats(data.stats)
    } catch (err) {
      toast.error('Could not fetch jobs. Is the backend running?')
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e?.preventDefault?.()
    runSearch()
  }

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-3xl sm:text-4xl font-bold">Find your next role</h1>
          <p className="mt-2 text-ink-600 dark:text-ink-400">
            Live job postings from LinkedIn, Indeed, Glassdoor, Naukri partners and more.
          </p>
        </motion.div>

        {/* Search Bar */}
        <form onSubmit={handleSubmit} className="card p-4 mt-6 grid lg:grid-cols-[1fr,1fr,auto] gap-3">
          <SearchAutocomplete
            value={query}
            onChange={setQuery}
            onSelect={(val) => runSearch(val)}
            onSubmit={() => runSearch()}
            placeholder="Job title or skill (e.g. Python developer)"
          />
          <div className="relative">
            <MapPin className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-400" size={18}/>
            <input
              type="text"
              value={location}
              onChange={e => setLocation(e.target.value)}
              placeholder="City (Bangalore, Mumbai, Hyderabad...)"
              disabled={globalSearch}
              className="input-field !pl-10 disabled:opacity-50"
            />
          </div>
          <button type="submit" className="btn-primary justify-center">
            {loading ? <RefreshCw size={16} className="animate-spin"/> : <Search size={16}/>}
            {loading ? 'Searching' : 'Search'}
          </button>
        </form>

        {/* Filters */}
        <div className="mt-3 flex flex-wrap gap-2 items-center text-sm">
          <span className="text-ink-500 flex items-center gap-1"><Filter size={14}/></span>
          <button
            onClick={() => setRemote(r => !r)}
            className={`px-3 py-1.5 rounded-lg border transition-colors flex items-center gap-1.5 ${
              remote ? 'bg-brand-600 text-white border-brand-600' : 'border-ink-300 dark:border-ink-700 hover:border-brand-500'
            }`}
          >
            <Wifi size={14}/> Remote only
          </button>
          <button
            onClick={() => setGlobalSearch(g => !g)}
            className={`px-3 py-1.5 rounded-lg border transition-colors flex items-center gap-1.5 ${
              globalSearch ? 'bg-brand-600 text-white border-brand-600' : 'border-ink-300 dark:border-ink-700 hover:border-brand-500'
            }`}
          >
            <Globe size={14}/> Global jobs
          </button>
        </div>

        {/* Stats Strip */}
        {stats && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-6 flex flex-wrap gap-3 text-sm">
            <div className="card px-4 py-2 flex items-center gap-2">
              <span className="font-semibold text-brand-600">{stats.total}</span>
              <span className="text-ink-500">jobs found</span>
            </div>
            {stats.remote_count > 0 && (
              <div className="card px-4 py-2 flex items-center gap-2">
                <span className="font-semibold text-green-600">{stats.remote_count}</span>
                <span className="text-ink-500">remote</span>
              </div>
            )}
            {Object.entries(stats.by_source || {}).map(([src, count]) => (
              <div key={src} className="card px-4 py-2 flex items-center gap-2 capitalize">
                <span className="font-semibold">{count}</span>
                <span className="text-ink-500">from {src}</span>
              </div>
            ))}
          </motion.div>
        )}

        {/* Results */}
        <div className="mt-6">
          {loading ? (
            <SkeletonGrid count={6}/>
          ) : results.length > 0 ? (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {results.map((job, i) => <JobCard key={job.job_id} job={job} index={i}/>)}
            </div>
          ) : hasSearched ? (
            <div className="card p-12 text-center">
              <p className="text-ink-500">No jobs found. Try a different keyword or expand to global search.</p>
            </div>
          ) : (
            <div className="card p-12 text-center">
              <Search className="mx-auto text-ink-300 mb-3" size={40}/>
              <p className="text-ink-500">Enter a search term to find live job postings.</p>
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  )
}
