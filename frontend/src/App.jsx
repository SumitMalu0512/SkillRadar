import { Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import AIChatWidget from './components/AIChatWidget'
import Landing from './pages/Landing'
import JobSearch from './pages/JobSearch'
import SkillsAnalytics from './pages/SkillsAnalytics'
import RoleExplorer from './pages/RoleExplorer'
import Forecast from './pages/Forecast'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import SavedJobs from './pages/SavedJobs'
import About from './pages/About'
import Login from './pages/Login'

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 relative">
        <AnimatePresence mode="wait">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/jobs" element={<JobSearch />} />
            <Route path="/skills" element={<SkillsAnalytics />} />
            <Route path="/roles" element={<RoleExplorer />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/resume" element={<ResumeAnalyzer />} />
            <Route path="/saved" element={<SavedJobs />} />
            <Route path="/about" element={<About />} />
            <Route path="/login" element={<Login />} />
          </Routes>
        </AnimatePresence>
      </main>
      <Footer />
      <AIChatWidget />
    </div>
  )
}
