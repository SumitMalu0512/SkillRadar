import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Mail, User, GraduationCap, ArrowRight } from 'lucide-react'
import toast from 'react-hot-toast'
import PageTransition from '../components/PageTransition'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [college, setCollege] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) return
    setLoading(true)
    try {
      await login(email, name, college)
      toast.success('Welcome to SkillRadar!')
      navigate('/jobs')
    } catch (err) {
      toast.error('Could not sign in. Check the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <PageTransition>
      <div className="max-w-md mx-auto px-4 py-16">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="text-center mb-8">
            <h1 className="font-display text-3xl font-bold">Welcome to SkillRadar</h1>
            <p className="text-ink-500 mt-2">Quick sign-in with your email — no password needed.</p>
          </div>

          <form onSubmit={handleSubmit} className="card p-6 space-y-4">
            <div>
              <label className="text-sm font-medium mb-1.5 block flex items-center gap-1.5"><Mail size={14}/> Email</label>
              <input
                type="email"
                required
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="input-field"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block flex items-center gap-1.5"><User size={14}/> Full name (optional)</label>
              <input
                type="text"
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Your full name"
                className="input-field"
              />
            </div>
            <div>
              <label className="text-sm font-medium mb-1.5 block flex items-center gap-1.5"><GraduationCap size={14}/> Organization (optional)</label>
              <input
                type="text"
                value={college}
                onChange={e => setCollege(e.target.value)}
                placeholder="Your organization"
                className="input-field"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full justify-center">
              {loading ? 'Signing in...' : 'Sign In'} <ArrowRight size={14}/>
            </button>
          </form>

          <p className="text-xs text-center text-ink-500 mt-6">
            By signing in you agree to use this academic project responsibly. Your email is only stored
            to associate saved jobs with your account.
          </p>
        </motion.div>
      </div>
    </PageTransition>
  )
}
