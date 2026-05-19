import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Bookmark, ArrowRight } from 'lucide-react'
import PageTransition from '../components/PageTransition'
import JobCard from '../components/JobCard'
import { SkeletonGrid } from '../components/Skeleton'
import { useAuth } from '../context/AuthContext'
import { userAPI } from '../lib/api'

export default function SavedJobs() {
  const { user, isAuthenticated } = useAuth()
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated) {
      setLoading(false)
      return
    }
    userAPI.saved(user.user_id)
      .then(d => setJobs(d.results || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [isAuthenticated, user])

  if (!isAuthenticated) {
    return (
      <PageTransition>
        <div className="max-w-2xl mx-auto px-4 py-20 text-center">
          <Bookmark className="mx-auto text-ink-300 mb-4" size={48}/>
          <h2 className="font-display text-2xl font-bold">Sign in to view saved jobs</h2>
          <p className="text-ink-500 mt-2">Bookmark jobs you're interested in and come back to them later.</p>
          <Link to="/login" className="btn-primary mt-6">Sign In <ArrowRight size={14}/></Link>
        </div>
      </PageTransition>
    )
  }

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 className="font-display text-3xl sm:text-4xl font-bold">Saved Jobs</h1>
        <p className="mt-2 text-ink-600 dark:text-ink-400">Your bookmarked opportunities, all in one place.</p>

        <div className="mt-8">
          {loading ? (
            <SkeletonGrid count={3}/>
          ) : jobs.length === 0 ? (
            <div className="card p-12 text-center">
              <Bookmark className="mx-auto text-ink-300 mb-3" size={40}/>
              <p className="text-ink-500">No saved jobs yet.</p>
              <Link to="/jobs" className="btn-primary mt-4 inline-flex">Browse Jobs</Link>
            </div>
          ) : (
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {jobs.map((j, i) => <JobCard key={j.job_id} job={j} index={i}/>)}
            </div>
          )}
        </div>
      </div>
    </PageTransition>
  )
}
