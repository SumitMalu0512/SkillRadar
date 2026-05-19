import { motion } from 'framer-motion'
import { Code, Database, Brain, Cloud, Zap, Globe, Search, BarChart3 } from 'lucide-react'
import PageTransition from '../components/PageTransition'

const tech = [
  { category: 'Frontend',  icon: Code,     items: ['React', 'Vite', 'Tailwind CSS', 'Framer Motion', 'Recharts'] },
  { category: 'Backend',   icon: Brain,    items: ['Python', 'Flask', 'spaCy', 'scikit-learn', 'Prophet'] },
  { category: 'Database',  icon: Database, items: ['PostgreSQL', 'Supabase'] },
  { category: 'Data Sources', icon: Cloud, items: ['Adzuna API', 'JSearch (RapidAPI)', 'Remotive API'] },
]

const methodology = [
  { step: 1, title: 'Data Collection',  desc: 'Live aggregation from multiple job APIs covering LinkedIn, Indeed, Glassdoor, Naukri network and remote-first companies.' },
  { step: 2, title: 'NLP Extraction',   desc: 'Custom skill taxonomy with 200+ canonical skills and 500+ aliases. Hybrid keyword and pattern matching with confidence scoring.' },
  { step: 3, title: 'Trend Analysis',   desc: 'Frequency analysis with growth rate computation. Tracks emerging vs declining skills across rolling time windows.' },
  { step: 4, title: 'Role Clustering',  desc: 'K-Means clustering on TF-IDF vectors of skill sets. Optimal cluster count determined via elbow method and silhouette score.' },
  { step: 5, title: 'Forecasting',      desc: 'Facebook Prophet time-series model for 90-day skill demand prediction with confidence intervals.' },
  { step: 6, title: 'Visualization',    desc: 'Interactive dashboards with real-time insights, light and dark themes, and full mobile responsiveness.' },
]

const stats = [
  { value: '50+',  label: 'Job Sources' },
  { value: '200+', label: 'Skills Tracked' },
  { value: '17',   label: 'Skill Categories' },
  { value: '90d',  label: 'Forecast Range' },
]

export default function About() {
  return (
    <PageTransition>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Hero */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-16">
          <h1 className="font-display text-4xl sm:text-5xl font-bold">About SkillRadar</h1>
          <p className="mt-4 text-lg text-ink-600 dark:text-ink-400 max-w-2xl mx-auto">
            A real-time job market intelligence platform combining live data aggregation,
            natural language processing, and machine learning to surface what actually matters in hiring today.
          </p>
        </motion.div>

        {/* Stats */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 10 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05 }}
              className="card p-6 text-center"
            >
              <div className="gradient-text font-display font-bold text-3xl sm:text-4xl">{s.value}</div>
              <div className="text-xs text-ink-500 mt-1">{s.label}</div>
            </motion.div>
          ))}
        </section>

        {/* Problem */}
        <section className="card p-8 mb-12">
          <h2 className="font-display text-2xl font-bold mb-4">The Problem</h2>
          <p className="text-ink-600 dark:text-ink-400 leading-relaxed">
            The job market evolves faster than anyone can manually track. New technologies emerge constantly,
            hiring patterns shift, and what was "in demand" six months ago may already be losing relevance.
            For someone trying to plan their career, learn the right skills, or understand where the market is heading,
            relying on outdated lists or generic advice is a losing strategy. SkillRadar automates this entire problem
            by analyzing live job posting data in real time and surfacing actionable insights.
          </p>
        </section>

        {/* How it works */}
        <section className="mb-12">
          <h2 className="font-display text-2xl font-bold mb-6">How It Works</h2>
          <div className="space-y-3">
            {methodology.map((m, i) => (
              <motion.div
                key={m.step}
                initial={{ opacity: 0, x: -10 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="card p-5 flex gap-4"
              >
                <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-gradient-to-br from-brand-500 to-brand-700 text-white font-bold flex items-center justify-center">
                  {m.step}
                </div>
                <div>
                  <h3 className="font-semibold">{m.title}</h3>
                  <p className="text-sm text-ink-600 dark:text-ink-400 mt-1">{m.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Features */}
        <section className="mb-12">
          <h2 className="font-display text-2xl font-bold mb-6">What You Can Do</h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {[
              { icon: Search, title: 'Live Job Search', desc: 'Search thousands of jobs across major portals from a single interface.' },
              { icon: BarChart3, title: 'Skills Analytics', desc: 'See which skills are trending, emerging, and declining right now.' },
              { icon: Globe, title: 'Role Discovery', desc: 'Explore natural role clusters revealed by machine learning.' },
              { icon: Zap, title: 'Demand Forecast', desc: '90-day predictions for skill demand based on historical patterns.' },
            ].map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="card p-5"
              >
                <div className="w-10 h-10 rounded-lg bg-brand-100 dark:bg-brand-900/30 flex items-center justify-center text-brand-600 dark:text-brand-400 mb-3">
                  <f.icon size={18}/>
                </div>
                <h3 className="font-semibold mb-1">{f.title}</h3>
                <p className="text-sm text-ink-600 dark:text-ink-400">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Tech Stack */}
        <section>
          <h2 className="font-display text-2xl font-bold mb-6">Built With</h2>
          <div className="grid sm:grid-cols-2 gap-4">
            {tech.map((t, i) => (
              <motion.div
                key={t.category}
                initial={{ opacity: 0, y: 10 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="card p-5"
              >
                <h3 className="font-semibold mb-3 flex items-center gap-2">
                  <t.icon size={16} className="text-brand-600"/>
                  {t.category}
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {t.items.map(i => <span key={i} className="badge-brand text-xs">{i}</span>)}
                </div>
              </motion.div>
            ))}
          </div>
        </section>
      </div>
    </PageTransition>
  )
}
