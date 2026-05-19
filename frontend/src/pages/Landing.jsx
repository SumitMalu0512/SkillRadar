import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Search, TrendingUp, Brain, BarChart3, Sparkles, ArrowRight, Zap, Globe,
  Database, Target, ShieldCheck, Users, Cpu,
} from 'lucide-react'
import PageTransition from '../components/PageTransition'
import SearchAutocomplete from '../components/SearchAutocomplete'
import AnimatedRadar from '../components/AnimatedRadar'
import AnimatedCounter from '../components/AnimatedCounter'
import { skillsAPI } from '../lib/api'

const features = [
  {
    icon: Search,
    title: 'Real-time Job Search',
    desc: 'Live data aggregated from LinkedIn, Indeed, Glassdoor, Naukri and 50+ sources.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: Brain,
    title: 'AI Skill Extraction',
    desc: 'NLP engine parses job descriptions and identifies in-demand skills automatically.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: TrendingUp,
    title: 'Trend Detection',
    desc: 'See which skills are rising, declining or newly emerging in the market.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: BarChart3,
    title: 'Role Clustering',
    desc: 'K-Means clustering groups similar job roles and reveals natural career paths.',
    color: 'from-amber-500 to-orange-500',
  },
  {
    icon: Zap,
    title: 'Demand Forecasting',
    desc: 'Time-series predictions for skill demand over the next 90 days.',
    color: 'from-rose-500 to-red-500',
  },
  {
    icon: Sparkles,
    title: 'AI Resume Analysis',
    desc: 'Upload your resume to find matching jobs, identify gaps, get AI suggestions.',
    color: 'from-violet-500 to-fuchsia-500',
  },
]

const stats = [
  { value: 200, suffix: '+', label: 'Skills Tracked' },
  { value: '1000+',  suffix: '',  label: 'Jobs Analyzed' },
  { value: 90,  suffix: 'd', label: 'Forecast Range' },
]

export default function Landing() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [topSkills, setTopSkills] = useState([])

  useEffect(() => {
    skillsAPI.top(10).then(d => setTopSkills(d.results || [])).catch(() => {})
  }, [])

  const handleSearch = (e) => {
    e?.preventDefault?.()
    if (query.trim()) {
      navigate(`/jobs?q=${encodeURIComponent(query)}`)
    } else {
      navigate('/jobs')
    }
  }

  return (
    <PageTransition>
      {/* ============= HERO ============= */}
      <section className="relative overflow-hidden bg-mesh">
        {/* Floating background blobs */}
        <div className="blob bg-brand-400/30 dark:bg-brand-500/30 w-[500px] h-[500px] top-[-200px] left-[-100px] float-slow"></div>
        <div className="blob bg-accent-500/20 w-[400px] h-[400px] top-[200px] right-[-100px] float-mid"></div>
        <div className="blob bg-purple-400/20 w-[450px] h-[450px] bottom-[-200px] left-[40%] float-fast"></div>

        {/* Grid overlay */}
        <div className="absolute inset-0 bg-grid opacity-50"></div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 sm:pt-24 sm:pb-28">
          <div className="grid lg:grid-cols-[1.1fr,1fr] gap-12 items-center">
            {/* Left: copy */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <motion.span
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="badge-brand inline-flex mb-6"
              >
                <Sparkles size={12} className="mr-1.5"/>
                Real-time Job Market Intelligence
              </motion.span>

              <h1 className="font-display text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold leading-[1.05] text-balance">
                Track the skills that{' '}
                <span className="gradient-text">get you hired</span>
              </h1>

              <p className="mt-6 text-lg text-ink-600 dark:text-ink-400 max-w-xl text-balance">
                SkillRadar analyzes thousands of live job postings to show you exactly
                what employers want — and what they'll want six months from now.
              </p>

              {/* Search */}
              <form onSubmit={handleSearch} className="mt-8 max-w-xl">
                <div className="flex items-stretch gap-2">
                  <div className="flex-1">
                    <SearchAutocomplete
                      value={query}
                      onChange={setQuery}
                      onSelect={(val) => navigate(`/jobs?q=${encodeURIComponent(val)}`)}
                      onSubmit={(val) => navigate(val?.trim() ? `/jobs?q=${encodeURIComponent(val)}` : '/jobs')}
                      placeholder="Search Python, React, Data Scientist..."
                      inputClassName="!py-3.5 !text-base shadow-xl shadow-brand-500/10"
                    />
                  </div>
                  <button type="submit" className="btn-primary px-5 shadow-xl shadow-brand-600/30">
                    <ArrowRight size={16}/>
                  </button>
                </div>

                {topSkills.length > 0 && (
                  <div className="mt-5 flex flex-wrap items-center gap-2 text-sm">
                    <span className="text-ink-500">Trending:</span>
                    {topSkills.slice(0, 5).map((s, i) => (
                      <motion.button
                        key={s.skill}
                        type="button"
                        initial={{ opacity: 0, y: 5 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.6 + i * 0.05 }}
                        onClick={() => navigate(`/jobs?q=${encodeURIComponent(s.skill)}`)}
                        className="badge-brand hover:scale-105 transition-transform cursor-pointer"
                      >
                        {s.skill}
                      </motion.button>
                    ))}
                  </div>
                )}
              </form>

              {/* Trust strip */}
              <div className="mt-10 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-ink-500">
                <div className="flex items-center gap-1.5"><ShieldCheck size={14} className="text-green-500"/> Live data</div>
                <div className="flex items-center gap-1.5"><Cpu size={14} className="text-brand-500"/> ML powered</div>
                <div className="flex items-center gap-1.5"><Globe size={14} className="text-purple-500"/> India-first</div>
              </div>
            </motion.div>

            {/* Right: animated radar */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex justify-center items-center"
            >
              <AnimatedRadar size={480} className="max-w-full"/>
            </motion.div>
          </div>
        </div>

        {/* Gradient fade to next section */}
        <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-b from-transparent to-ink-50 dark:to-ink-950 pointer-events-none"></div>
      </section>

      {/* ============= STATS STRIP ============= */}
      <section className="relative -mt-12 z-10">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-card p-6 grid grid-cols-3 gap-4"
          >
            {stats.map((s, i) => (
              <div key={s.label} className="text-center">
                <div className="font-display text-3xl sm:text-4xl font-bold gradient-text">
                  <AnimatedCounter value={s.value} suffix={s.suffix} duration={1600 + i * 100}/>
                </div>
                <div className="text-xs text-ink-500 mt-1 uppercase tracking-wide">{s.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ============= FEATURES ============= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-100px' }}
          className="text-center mb-14 max-w-2xl mx-auto"
        >
          <span className="badge-brand inline-flex mb-4">
            <Zap size={11} className="mr-1"/> What it does
          </span>
          <h2 className="font-display text-3xl sm:text-5xl font-bold text-balance">
            Everything you need to{' '}
            <span className="gradient-text">navigate the market</span>
          </h2>
          <p className="mt-4 text-ink-600 dark:text-ink-400 text-balance">
            From raw job data to actionable career insights — all in one platform.
          </p>
        </motion.div>

        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-50px' }}
              transition={{ delay: i * 0.05 }}
              whileHover={{ y: -6 }}
              className="card p-6 hover-glow group"
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${f.color} flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform shadow-lg`}>
                <f.icon size={22}/>
              </div>
              <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
              <p className="text-sm text-ink-600 dark:text-ink-400 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ============= HOW IT WORKS ============= */}
      <section className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-14"
        >
          <span className="badge-brand inline-flex mb-4">
            <Brain size={11} className="mr-1"/> The pipeline
          </span>
          <h2 className="font-display text-3xl sm:text-5xl font-bold text-balance">
            From job posting to{' '}
            <span className="gradient-text">career insight</span>
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6 relative">
          {/* connecting line */}
          <div className="hidden md:block absolute top-12 left-[16%] right-[16%] h-px bg-gradient-to-r from-transparent via-brand-500/50 to-transparent"></div>

          {[
            { num: '01', title: 'Collect', desc: 'Live job data aggregated from Adzuna, JSearch, Remotive and more.', icon: Database },
            { num: '02', title: 'Analyze',  desc: 'NLP extracts skills, K-Means clusters roles, Prophet forecasts demand.', icon: Cpu },
            { num: '03', title: 'Visualize', desc: 'Interactive dashboards and AI chat reveal patterns instantly.', icon: BarChart3 },
          ].map((step, i) => (
            <motion.div
              key={step.num}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="relative card p-6 text-center hover-glow"
            >
              <div className="relative inline-flex">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white shadow-xl shadow-brand-600/30 relative z-10">
                  <step.icon size={32}/>
                </div>
                {/* pulse ring */}
                <div className="absolute inset-0 rounded-full bg-brand-500/40 pulse-ring"></div>
              </div>
              <div className="mt-4 text-xs font-mono text-brand-500/60 tracking-widest">STEP {step.num}</div>
              <h3 className="font-display text-xl font-bold mt-1">{step.title}</h3>
              <p className="text-sm text-ink-600 dark:text-ink-400 mt-2">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ============= CTA ============= */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 pb-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="relative overflow-hidden rounded-3xl p-10 sm:p-16"
        >
          {/* mesh gradient bg */}
          <div className="absolute inset-0 bg-gradient-to-br from-brand-600 via-brand-700 to-brand-900"></div>
          <div className="absolute inset-0 opacity-30" style={{
            backgroundImage: 'radial-gradient(at 0% 0%, rgba(245,158,11,0.5) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(168,85,247,0.5) 0px, transparent 50%)',
          }}></div>

          {/* radar overlay */}
          <div className="absolute -right-32 -bottom-32 opacity-20">
            <AnimatedRadar size={400}/>
          </div>

          <div className="relative text-center max-w-2xl mx-auto">
            <h2 className="font-display text-3xl sm:text-5xl font-bold text-white text-balance">
              Start exploring the job market intelligently
            </h2>
            <p className="mt-4 text-brand-100 text-balance">
              Search live jobs, discover trending skills, get AI-powered resume insights.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-3">
              <Link to="/jobs" className="px-6 py-3 rounded-lg bg-white text-brand-700 font-medium hover:bg-brand-50 transition-all hover:scale-105 inline-flex items-center gap-2 shadow-xl">
                <Search size={16}/> Browse Jobs
              </Link>
              <Link to="/resume" className="px-6 py-3 rounded-lg bg-brand-800/50 text-white border border-white/20 hover:bg-brand-800 transition-all hover:scale-105 inline-flex items-center gap-2 backdrop-blur-sm">
                <Sparkles size={16}/> Try Resume AI
              </Link>
            </div>
          </div>
        </motion.div>
      </section>
    </PageTransition>
  )
}
