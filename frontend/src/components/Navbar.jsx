import { useState, useEffect } from 'react'
import { Link, NavLink, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Sun, Moon, Menu, X, LogOut, Bookmark } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'

const nav = [
  { to: '/jobs', label: 'Jobs' },
  { to: '/skills', label: 'Skills' },
  { to: '/roles', label: 'Roles' },
  { to: '/forecast', label: 'Forecast' },
  { to: '/resume', label: 'Resume AI', badge: 'AI' },
  { to: '/about', label: 'About' },
]

export default function Navbar() {
  const { theme, toggle } = useTheme()
  const { user, logout, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  // close menu when route changes
  useEffect(() => {
    setOpen(false)
    setMenuOpen(false)
  }, [location.pathname])

  // detect scroll for frosted-glass intensity
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10)
    window.addEventListener('scroll', onScroll)
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 ${
      scrolled
        ? 'backdrop-blur-xl bg-white/70 dark:bg-ink-950/70 shadow-sm'
        : 'backdrop-blur-md bg-white/50 dark:bg-ink-950/50'
    } border-b border-ink-200/50 dark:border-ink-800/50`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2 group">
            <motion.div
              whileHover={{ rotate: 90, scale: 1.1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="relative w-9 h-9 rounded-xl bg-gradient-to-br from-brand-500 via-brand-600 to-brand-800 flex items-center justify-center shadow-lg shadow-brand-600/30"
            >
              <svg viewBox="0 0 24 24" className="w-5 h-5 text-white" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <circle cx="12" cy="12" r="6" opacity="0.6"/>
                <circle cx="12" cy="12" r="2" fill="currentColor"/>
                <path d="M12 12 L19 5" strokeLinecap="round"/>
              </svg>
            </motion.div>
            <span className="font-display font-bold text-lg">
              Skill<span className="gradient-text">Radar</span>
            </span>
          </Link>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1 bg-ink-100/50 dark:bg-ink-900/50 rounded-full p-1">
            {nav.map(n => (
              <NavLink
                key={n.to}
                to={n.to}
                className={({ isActive }) =>
                  `relative px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    isActive
                      ? 'text-white'
                      : 'text-ink-600 hover:text-ink-900 dark:text-ink-400 dark:hover:text-ink-100'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <motion.span
                        layoutId="active-nav-pill"
                        className="absolute inset-0 bg-gradient-to-br from-brand-600 to-brand-700 rounded-full shadow-md shadow-brand-600/30"
                        transition={{ type: 'spring', stiffness: 380, damping: 30 }}
                      />
                    )}
                    <span className="relative z-10 flex items-center gap-1.5">
                      {n.label}
                      {n.badge && (
                        <span className={`px-1.5 py-0.5 text-[9px] font-bold rounded-full ${
                          isActive ? 'bg-white/20 text-white' : 'bg-gradient-to-r from-accent-500 to-amber-500 text-white'
                        }`}>
                          {n.badge}
                        </span>
                      )}
                    </span>
                  </>
                )}
              </NavLink>
            ))}
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-2">
            <button
              onClick={toggle}
              className="p-2 rounded-lg hover:bg-ink-100 dark:hover:bg-ink-800 transition-colors"
              aria-label="Toggle theme"
            >
              <motion.div
                key={theme}
                initial={{ rotate: -180, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                transition={{ duration: 0.3 }}
              >
                {theme === 'dark' ? <Sun size={18}/> : <Moon size={18}/>}
              </motion.div>
            </button>

            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setMenuOpen(o => !o)}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-ink-100 dark:hover:bg-ink-800 transition-colors"
                >
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-brand-500 to-accent-500 flex items-center justify-center text-white text-xs font-bold shadow-md">
                    {user?.email?.[0]?.toUpperCase() || 'U'}
                  </div>
                  <span className="hidden sm:inline text-sm">{user?.email?.split('@')[0]}</span>
                </button>
                {menuOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -8, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ duration: 0.15 }}
                    className="absolute right-0 mt-2 w-48 py-1 glass-card overflow-hidden"
                  >
                    <Link to="/saved" onClick={() => setMenuOpen(false)} className="flex items-center gap-2 px-4 py-2 text-sm hover:bg-brand-50 dark:hover:bg-ink-800/50">
                      <Bookmark size={14}/> Saved Jobs
                    </Link>
                    <button onClick={() => { logout(); setMenuOpen(false); navigate('/') }} className="w-full flex items-center gap-2 px-4 py-2 text-sm hover:bg-brand-50 dark:hover:bg-ink-800/50 text-left">
                      <LogOut size={14}/> Sign Out
                    </button>
                  </motion.div>
                )}
              </div>
            ) : (
              <Link to="/login" className="btn-primary text-sm hidden sm:inline-flex">
                Sign In
              </Link>
            )}

            <button onClick={() => setOpen(o => !o)} className="md:hidden p-2 rounded-lg hover:bg-ink-100 dark:hover:bg-ink-800">
              {open ? <X size={20}/> : <Menu size={20}/>}
            </button>
          </div>
        </div>

        {/* Mobile nav */}
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="md:hidden py-3 border-t border-ink-200 dark:border-ink-800 overflow-hidden"
          >
            {nav.map(n => (
              <NavLink
                key={n.to}
                to={n.to}
                onClick={() => setOpen(false)}
                className={({ isActive }) =>
                  `flex items-center justify-between px-4 py-2.5 ${isActive ? 'text-brand-600 dark:text-brand-400 font-medium' : 'text-ink-600 dark:text-ink-400'}`
                }
              >
                <span>{n.label}</span>
                {n.badge && (
                  <span className="px-1.5 py-0.5 text-[9px] font-bold rounded-full bg-gradient-to-r from-accent-500 to-amber-500 text-white">
                    {n.badge}
                  </span>
                )}
              </NavLink>
            ))}
            {!isAuthenticated && (
              <Link to="/login" onClick={() => setOpen(false)} className="block px-4 py-2 text-brand-600 font-medium">
                Sign In
              </Link>
            )}
          </motion.div>
        )}
      </div>
    </header>
  )
}
