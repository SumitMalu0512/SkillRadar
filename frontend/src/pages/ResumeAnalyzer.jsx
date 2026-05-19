import { useState, useCallback, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Upload, FileText, Sparkles, Target, TrendingUp, AlertCircle,
  CheckCircle2, X, Award, Brain, ChevronRight, Loader2, Copy, RefreshCw,
  ExternalLink,
} from 'lucide-react'
import toast from 'react-hot-toast'
import PageTransition from '../components/PageTransition'
import JobCard from '../components/JobCard'
import { aiAPI } from '../lib/api'

export default function ResumeAnalyzer() {
  const [file, setFile] = useState(null)
  const [dragOver, setDragOver] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState(null)
  const fileInputRef = useRef(null)

  const handleFile = (f) => {
    if (!f) return
    if (!f.name.toLowerCase().endsWith('.pdf')) {
      toast.error('Please upload a PDF file')
      return
    }
    if (f.size > 10 * 1024 * 1024) {
      toast.error('File too large (max 10 MB)')
      return
    }
    setFile(f)
    analyze(f)
  }

  const analyze = async (f) => {
    setAnalyzing(true)
    setResult(null)
    try {
      const data = await aiAPI.analyzeResume(f)
      if (data.error) {
        toast.error(data.error)
      } else {
        setResult(data)
        toast.success(`Found ${data.resume.skills.length} skills in your resume`)
      }
    } catch (err) {
      const errMsg = err.response?.data?.error || 'Could not analyze resume'
      toast.error(errMsg)
    } finally {
      setAnalyzing(false)
    }
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    handleFile(f)
  }, [])

  const reset = () => {
    setFile(null)
    setResult(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  return (
    <PageTransition>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <span className="badge-brand mb-3 inline-flex">
            <Sparkles size={12} className="mr-1"/> AI-Powered Resume Analysis
          </span>
          <h1 className="font-display text-3xl sm:text-4xl font-bold">Resume Analyzer</h1>
          <p className="mt-2 text-ink-600 dark:text-ink-400 max-w-2xl">
            Upload your resume to discover matching jobs, identify skill gaps, and get AI-generated suggestions to tailor your resume for any role.
          </p>
        </motion.div>

        {!result ? (
          <UploadZone
            onFile={handleFile}
            file={file}
            analyzing={analyzing}
            dragOver={dragOver}
            setDragOver={setDragOver}
            onDrop={handleDrop}
            fileInputRef={fileInputRef}
            onReset={reset}
          />
        ) : (
          <ResultView result={result} onReset={reset}/>
        )}
      </div>
    </PageTransition>
  )
}

function UploadZone({ onFile, file, analyzing, dragOver, setDragOver, onDrop, fileInputRef, onReset }) {
  return (
    <div className="mt-8 max-w-2xl mx-auto">
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => !analyzing && fileInputRef.current?.click()}
        className={`relative cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all ${
          dragOver
            ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/20 scale-[1.01]'
            : 'border-ink-300 dark:border-ink-700 hover:border-brand-400'
        } ${analyzing ? 'pointer-events-none opacity-70' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={(e) => onFile(e.target.files[0])}
          className="hidden"
        />

        {analyzing ? (
          <div className="space-y-3">
            <Loader2 size={48} className="mx-auto text-brand-500 animate-spin"/>
            <p className="font-medium">Analyzing your resume...</p>
            <p className="text-sm text-ink-500">Extracting skills · Finding matches · Computing gaps</p>
          </div>
        ) : file ? (
          <div className="space-y-3">
            <FileText size={48} className="mx-auto text-brand-500"/>
            <p className="font-semibold">{file.name}</p>
            <p className="text-sm text-ink-500">{(file.size / 1024).toFixed(1)} KB</p>
            <button
              onClick={(e) => { e.stopPropagation(); onReset() }}
              className="text-sm text-ink-500 hover:text-red-500"
            >
              Choose a different file
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="w-16 h-16 mx-auto rounded-2xl bg-brand-100 dark:bg-brand-900/30 flex items-center justify-center">
              <Upload size={28} className="text-brand-600 dark:text-brand-400"/>
            </div>
            <div>
              <p className="font-semibold text-lg">Drop your resume here</p>
              <p className="text-sm text-ink-500 mt-1">or click to browse</p>
            </div>
            <p className="text-xs text-ink-400 mt-4">PDF only · Max 10 MB · Your file stays private</p>
          </div>
        )}
      </div>

      <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-3">
        {[
          { icon: Brain, title: 'Skill Extraction', desc: 'NLP identifies your skills automatically' },
          { icon: Target, title: 'Job Matching', desc: 'Find roles that match your profile' },
          { icon: Sparkles, title: 'AI Suggestions', desc: 'Tailor your resume per job with AI' },
        ].map((f) => (
          <div key={f.title} className="text-center p-4">
            <f.icon size={20} className="mx-auto text-brand-600 mb-2"/>
            <p className="font-semibold text-sm">{f.title}</p>
            <p className="text-xs text-ink-500 mt-1">{f.desc}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function ResultView({ result, onReset }) {
  const [tab, setTab] = useState('matches')
  const { resume, matched_jobs, skill_gaps, strengths, stats } = result

  return (
    <div className="mt-8 space-y-6">
      {/* Resume summary card */}
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="card p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center text-xl font-bold">
                {(resume.name || 'Y').charAt(0).toUpperCase()}
              </div>
              <div>
                <h2 className="font-display text-xl font-bold">
                  {resume.name || 'Your Resume'}
                </h2>
                {resume.email && <p className="text-sm text-ink-500">{resume.email}</p>}
              </div>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              <span className="badge-brand">
                <Brain size={11} className="mr-1"/> {resume.skills.length} skills found
              </span>
              {resume.experience_years && (
                <span className="badge bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
                  {resume.experience_years}+ years experience
                </span>
              )}
              {resume.experience_level && resume.experience_level !== 'unspecified' && (
                <span className="badge bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 capitalize">
                  {resume.experience_level}
                </span>
              )}
              {resume.target_roles?.slice(0, 2).map(r => (
                <span key={r} className="badge bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300">
                  <Target size={11} className="mr-1"/> {r}
                </span>
              ))}
            </div>
          </div>

          <button onClick={onReset} className="btn-secondary text-sm">
            <RefreshCw size={14}/> Upload different resume
          </button>
        </div>

        {/* Quick stats */}
        <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-3">
          <Stat label="Skills detected" value={resume.skills.length}/>
          <Stat label="Matching jobs" value={matched_jobs?.length || 0}/>
          <Stat label="Avg match score" value={`${stats?.avg_match_score || 0}%`}/>
          <Stat label="Skills to learn" value={skill_gaps?.length || 0}/>
        </div>
      </motion.div>

      {/* Tabs */}
      <div className="flex flex-wrap gap-2">
        {[
          { id: 'matches', label: `Matching Jobs (${matched_jobs?.length || 0})`, icon: Target },
          { id: 'skills',  label: `Your Skills (${resume.skills.length})`, icon: Brain },
          { id: 'gaps',    label: `Skills to Learn (${skill_gaps?.length || 0})`, icon: TrendingUp },
          { id: 'strengths', label: `Your Strengths (${strengths?.length || 0})`, icon: Award },
        ].map(t => (
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

      <AnimatePresence mode="wait">
        {tab === 'matches' && (
          <motion.div key="matches" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <MatchesView jobs={matched_jobs} resume={resume}/>
          </motion.div>
        )}
        {tab === 'skills' && (
          <motion.div key="skills" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <SkillsView skillDetails={resume.skill_details}/>
          </motion.div>
        )}
        {tab === 'gaps' && (
          <motion.div key="gaps" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <GapsView gaps={skill_gaps}/>
          </motion.div>
        )}
        {tab === 'strengths' && (
          <motion.div key="strengths" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <StrengthsView strengths={strengths}/>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

function Stat({ label, value }) {
  return (
    <div className="p-3 rounded-lg bg-ink-50 dark:bg-ink-800/60 text-center">
      <div className="text-xs text-ink-500">{label}</div>
      <div className="text-xl font-bold mt-0.5">{value}</div>
    </div>
  )
}

function MatchesView({ jobs, resume }) {
  const [selectedJob, setSelectedJob] = useState(null)
  if (!jobs || jobs.length === 0) {
    return <div className="card p-8 text-center text-ink-500">No matching jobs found yet.</div>
  }
  return (
    <>
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {jobs.slice(0, 12).map((j, i) => (
          <MatchedJobCard key={j.job_id} job={j} index={i} onTailor={() => setSelectedJob(j)}/>
        ))}
      </div>
      <AnimatePresence>
        {selectedJob && (
          <TailorModal
            job={selectedJob}
            resume={resume}
            onClose={() => setSelectedJob(null)}
          />
        )}
      </AnimatePresence>
    </>
  )
}

function MatchedJobCard({ job, index, onTailor }) {
  const score = job.match_score || 0
  const scoreColor = score >= 75 ? 'text-green-600 dark:text-green-400'
    : score >= 50 ? 'text-amber-600 dark:text-amber-400'
    : 'text-red-600 dark:text-red-400'
  const scoreBg = score >= 75 ? 'bg-green-100 dark:bg-green-900/30'
    : score >= 50 ? 'bg-amber-100 dark:bg-amber-900/30'
    : 'bg-red-100 dark:bg-red-900/30'

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.04, 0.4) }}
      className="card p-5 flex flex-col"
    >
      <div className="flex justify-between items-start gap-2 mb-2">
        <h3 className="font-semibold leading-snug flex-1 line-clamp-2">{job.title}</h3>
        <div className={`flex-shrink-0 px-2.5 py-1 rounded-lg text-sm font-bold ${scoreBg} ${scoreColor}`}>
          {score.toFixed(0)}%
        </div>
      </div>
      <p className="text-sm text-ink-500 mb-3">{job.company} · {job.location}</p>

      {job.matched_skills?.length > 0 && (
        <div className="mb-2">
          <p className="text-xs text-ink-400 mb-1">✓ You have:</p>
          <div className="flex flex-wrap gap-1">
            {job.matched_skills.slice(0, 5).map(s => (
              <span key={s} className="badge bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300 text-xs">{s}</span>
            ))}
          </div>
        </div>
      )}
      {job.missing_skills?.length > 0 && (
        <div className="mb-3">
          <p className="text-xs text-ink-400 mb-1">✗ Missing:</p>
          <div className="flex flex-wrap gap-1">
            {job.missing_skills.slice(0, 4).map(s => (
              <span key={s} className="badge bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300 text-xs">{s}</span>
            ))}
          </div>
        </div>
      )}

      <div className="mt-auto pt-3 border-t border-ink-100 dark:border-ink-800 flex gap-2">
        <a href={job.source_url} target="_blank" rel="noopener noreferrer" className="btn-secondary text-xs flex-1 justify-center">
          View Job
        </a>
        <button onClick={onTailor} className="btn-primary text-xs flex-1 justify-center">
          <Sparkles size={12}/> AI Tailor
        </button>
      </div>
    </motion.div>
  )
}

function TailorModal({ job, resume, onClose }) {
  const [loading, setLoading] = useState(true)
  const [suggestions, setSuggestions] = useState('')
  const [source, setSource] = useState('')

  const generate = async () => {
    setLoading(true)
    try {
      const data = await aiAPI.tailorResume({
        resume_text: resume.skills.join(', ') + '\n\n' + (resume.target_roles || []).join(', '),
        user_skills: resume.skills,
        job_id: job.job_id,
      })
      setSuggestions(data.suggestions || 'No suggestions generated.')
      setSource(data.source || '')
    } catch (err) {
      toast.error('Could not generate suggestions')
      setSuggestions('Failed to generate suggestions. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // run on mount
  useState(() => { generate() })

  const copyText = () => {
    navigator.clipboard.writeText(suggestions)
    toast.success('Copied to clipboard')
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      onClick={onClose}
      className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4"
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="card p-6 max-w-2xl w-full max-h-[85vh] overflow-y-auto"
      >
        <div className="flex items-start justify-between gap-3 mb-4">
          <div>
            <span className="badge-brand mb-2 inline-flex">
              <Sparkles size={11} className="mr-1"/> AI Resume Tailoring
            </span>
            <h2 className="text-xl font-display font-bold">{job.title}</h2>
            <p className="text-sm text-ink-500">{job.company} · {job.match_score?.toFixed(0)}% match</p>
          </div>
          <button onClick={onClose} className="p-2 hover:bg-ink-100 dark:hover:bg-ink-800 rounded-lg">
            <X size={18}/>
          </button>
        </div>

        {loading ? (
          <div className="py-12 text-center">
            <Loader2 size={36} className="mx-auto text-brand-500 animate-spin mb-3"/>
            <p className="font-medium">AI is analyzing the job and your resume...</p>
            <p className="text-sm text-ink-500 mt-1">This takes 5-10 seconds</p>
          </div>
        ) : (
          <>
            <div className="bg-ink-50 dark:bg-ink-800/50 rounded-lg p-4 whitespace-pre-wrap text-sm leading-relaxed">
              {suggestions}
            </div>

            {source === 'fallback' && (
              <div className="mt-3 p-3 rounded-lg bg-amber-50 dark:bg-amber-900/20 text-xs text-amber-700 dark:text-amber-300 flex items-start gap-2">
                <AlertCircle size={14} className="flex-shrink-0 mt-0.5"/>
                <span>Using fallback suggestions. For AI-powered tailoring, set up a Groq API key in your environment.</span>
              </div>
            )}

            <div className="mt-4 flex gap-2">
              <button onClick={copyText} className="btn-secondary text-sm flex-1 justify-center">
                <Copy size={14}/> Copy
              </button>
              <button onClick={generate} className="btn-secondary text-sm flex-1 justify-center">
                <RefreshCw size={14}/> Regenerate
              </button>
            </div>
          </>
        )}
      </motion.div>
    </motion.div>
  )
}

function SkillsView({ skillDetails }) {
  if (!skillDetails || skillDetails.length === 0) {
    return <div className="card p-8 text-center text-ink-500">No skills extracted.</div>
  }
  // group by category
  const grouped = {}
  for (const d of skillDetails) {
    const cat = d.category || 'Other'
    if (!grouped[cat]) grouped[cat] = []
    grouped[cat].push(d)
  }
  return (
    <div className="grid sm:grid-cols-2 gap-4">
      {Object.entries(grouped).map(([cat, items]) => (
        <div key={cat} className="card p-5">
          <h3 className="font-semibold mb-3 flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-brand-500"></span>
            {cat} <span className="text-xs text-ink-400 font-normal">({items.length})</span>
          </h3>
          <div className="flex flex-wrap gap-1.5">
            {items.map(d => (
              <span key={d.skill} className="badge-brand text-xs" title={`${d.mention_count} mentions`}>{d.skill}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function GapsView({ gaps }) {
  const [expandedSkill, setExpandedSkill] = useState(null)
  if (!gaps || gaps.length === 0) {
    return <div className="card p-8 text-center text-ink-500">Great coverage! No major skill gaps detected.</div>
  }
  return (
    <div className="card p-6">
      <p className="text-sm text-ink-600 dark:text-ink-400 mb-4">
        These skills appear frequently in jobs but are missing from your resume. Click any skill to see learning resources.
      </p>
      <div className="space-y-2">
        {gaps.map((g, i) => {
          const isOpen = expandedSkill === g.skill
          return (
            <motion.div
              key={g.skill}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.04 }}
              className="rounded-lg border border-ink-200 dark:border-ink-800 overflow-hidden"
            >
              <button
                onClick={() => setExpandedSkill(isOpen ? null : g.skill)}
                className="w-full flex items-center gap-4 p-3 hover:bg-ink-50 dark:hover:bg-ink-800/50 text-left transition-colors"
              >
                <span className="w-8 text-ink-400 text-sm">#{i + 1}</span>
                <div className="flex-1">
                  <div className="font-medium">{g.skill}</div>
                  <div className="text-xs text-ink-500">Required by {g.missing_in_jobs} jobs ({g.percentage}%)</div>
                </div>
                <div className="w-32 hidden sm:block">
                  <div className="h-1.5 bg-ink-200 dark:bg-ink-800 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${Math.min(g.percentage * 2, 100)}%` }}
                      transition={{ duration: 0.6, delay: i * 0.05 }}
                      className="h-full bg-gradient-to-r from-red-400 to-amber-500"
                    />
                  </div>
                </div>
                <ChevronRight
                  size={16}
                  className={`text-ink-400 transition-transform ${isOpen ? 'rotate-90' : ''}`}
                />
              </button>
              <AnimatePresence>
                {isOpen && g.learning_resources && g.learning_resources.length > 0 && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden border-t border-ink-200 dark:border-ink-800 bg-ink-50/50 dark:bg-ink-900/30"
                  >
                    <div className="p-4 space-y-2">
                      <p className="text-xs font-semibold text-ink-500 uppercase tracking-wide">Learn this skill:</p>
                      {g.learning_resources.map((r) => (
                        <a
                          key={r.url}
                          href={r.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-3 p-2.5 rounded-lg bg-white dark:bg-ink-900 border border-ink-200 dark:border-ink-700 hover:border-brand-500 transition-colors group"
                        >
                          <ResourceIcon type={r.type}/>
                          <div className="flex-1 min-w-0">
                            <div className="text-sm font-medium group-hover:text-brand-600 dark:group-hover:text-brand-400 truncate">
                              {r.title}
                            </div>
                            <div className="text-xs text-ink-500 capitalize">{r.type}</div>
                          </div>
                          <ExternalLink size={14} className="text-ink-400 group-hover:text-brand-500"/>
                        </a>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}

function ResourceIcon({ type }) {
  const iconMap = {
    course:   { bg: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400', label: 'C' },
    tutorial: { bg: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400', label: 'T' },
    docs:     { bg: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400', label: 'D' },
    videos:   { bg: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400', label: 'V' },
    practice: { bg: 'bg-amber-100 text-amber-600 dark:bg-amber-900/30 dark:text-amber-400', label: 'P' },
  }
  const cfg = iconMap[type] || iconMap.tutorial
  return (
    <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${cfg.bg}`}>
      {cfg.label}
    </div>
  )
}

function StrengthsView({ strengths }) {
  if (!strengths || strengths.length === 0) {
    return <div className="card p-8 text-center text-ink-500">No marketable strengths detected yet.</div>
  }
  return (
    <div className="card p-6">
      <p className="text-sm text-ink-600 dark:text-ink-400 mb-4">
        These are your most marketable skills based on current job market demand.
      </p>
      <div className="space-y-2">
        {strengths.map((s, i) => (
          <motion.div
            key={s.skill}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.04 }}
            className="flex items-center gap-4 p-3 rounded-lg hover:bg-ink-50 dark:hover:bg-ink-800/50"
          >
            <CheckCircle2 size={18} className="text-green-500 flex-shrink-0"/>
            <div className="flex-1">
              <div className="font-medium">{s.skill}</div>
              <div className="text-xs text-ink-500">Demanded by {s.demand} jobs ({s.percentage}%)</div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
