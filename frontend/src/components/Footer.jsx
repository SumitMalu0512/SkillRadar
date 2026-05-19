import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="border-t border-ink-200 dark:border-ink-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center">
                <svg viewBox="0 0 24 24" className="w-4 h-4 text-white" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <circle cx="12" cy="12" r="2" fill="currentColor" />
                  <path d="M12 12 L19 5" strokeLinecap="round" />
                </svg>
              </div>
              <span className="font-display font-bold">Skill<span className="gradient-text">Radar</span></span>
            </div>
            <p className="text-sm text-ink-600 dark:text-ink-400 max-w-md">
              Real-time job market intelligence platform. Track in-demand skills, discover trending roles, and forecast future demand using live data and machine learning.
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-sm mb-3">Explore</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/jobs" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">Job Search</Link></li>
              <li><Link to="/skills" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">Skills Analytics</Link></li>
              <li><Link to="/roles" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">Role Clusters</Link></li>
              <li><Link to="/forecast" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">Forecast</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-sm mb-3">Platform</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/about" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">About</Link></li>
              <li><Link to="/saved" className="text-ink-600 dark:text-ink-400 hover:text-brand-600">Saved Jobs</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-ink-200 dark:border-ink-800 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs text-ink-500">
          <p>© 2026 SkillRadar. All rights reserved.</p>
          <p>Real-time data from leading job platforms.</p>
        </div>
      </div>
    </footer>
  )
}
