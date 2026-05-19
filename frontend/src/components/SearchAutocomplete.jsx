import { useState, useEffect, useRef, useCallback } from 'react'
import { Search, Briefcase, Code2, Building2, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { suggestAPI } from '../lib/api'

const typeIcon = {
  skill:   Code2,
  role:    Briefcase,
  company: Building2,
}

const typeLabel = {
  skill:   'Skill',
  role:    'Role',
  company: 'Company',
}

const typeColor = {
  skill:   'text-brand-600 dark:text-brand-400',
  role:    'text-amber-600 dark:text-amber-400',
  company: 'text-green-600 dark:text-green-400',
}

/**
 * SearchAutocomplete
 *  - value/onChange: controlled input
 *  - onSelect: called with the selected suggestion value when user picks one
 *  - onSubmit: called when user presses Enter or clicks the search icon
 */
export default function SearchAutocomplete({
  value,
  onChange,
  onSelect,
  onSubmit,
  placeholder = "Search...",
  autoFocus = false,
  className = "",
  inputClassName = "",
}) {
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [activeIndex, setActiveIndex] = useState(-1)
  const [loading, setLoading] = useState(false)
  const inputRef = useRef(null)
  const containerRef = useRef(null)
  const abortRef = useRef(null)
  const debounceRef = useRef(null)

  // Debounced fetch when value changes
  useEffect(() => {
    // cancel any pending request and any pending timer
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (abortRef.current) abortRef.current.abort()

    const trimmed = value?.trim()
    if (!trimmed || trimmed.length < 1) {
      setSuggestions([])
      setLoading(false)
      return
    }

    setLoading(true)
    debounceRef.current = setTimeout(async () => {
      try {
        const controller = new AbortController()
        abortRef.current = controller
        const data = await suggestAPI.query(trimmed, 8)
        setSuggestions(data.suggestions || [])
        setActiveIndex(-1)
      } catch (e) {
        // ignore errors silently - bad UX to alert on every keystroke
        setSuggestions([])
      } finally {
        setLoading(false)
      }
    }, 180)  // 180ms debounce - sweet spot for responsiveness

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [value])

  // Close dropdown when clicking outside
  useEffect(() => {
    const handler = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setShowSuggestions(false)
      }
    }
    document.addEventListener('mousedown', handler)
    return () => document.removeEventListener('mousedown', handler)
  }, [])

  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter') {
        e.preventDefault()
        onSubmit?.(value)
      }
      return
    }

    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setActiveIndex(i => Math.min(i + 1, suggestions.length - 1))
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setActiveIndex(i => Math.max(i - 1, -1))
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (activeIndex >= 0 && suggestions[activeIndex]) {
        handlePick(suggestions[activeIndex])
      } else {
        onSubmit?.(value)
        setShowSuggestions(false)
      }
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
    }
  }

  const handlePick = useCallback((sugg) => {
    onChange(sugg.value)
    onSelect?.(sugg.value)
    setShowSuggestions(false)
    setActiveIndex(-1)
  }, [onChange, onSelect])

  const handleClear = () => {
    onChange('')
    setSuggestions([])
    setActiveIndex(-1)
    inputRef.current?.focus()
  }

  return (
    <div ref={containerRef} className={`relative ${className}`}>
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-ink-400 pointer-events-none" size={18}/>
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={(e) => { onChange(e.target.value); setShowSuggestions(true) }}
          onFocus={() => setShowSuggestions(true)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          autoFocus={autoFocus}
          className={`input-field !pl-10 !pr-10 ${inputClassName}`}
          autoComplete="off"
          spellCheck="false"
        />
        {value && (
          <button
            onClick={handleClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-ink-400 hover:text-ink-600 dark:hover:text-ink-200"
            type="button"
            aria-label="Clear"
          >
            <X size={16}/>
          </button>
        )}
      </div>

      <AnimatePresence>
        {showSuggestions && (suggestions.length > 0 || loading) && (
          <motion.div
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -4 }}
            transition={{ duration: 0.12 }}
            className="absolute z-50 left-0 right-0 mt-2 card overflow-hidden shadow-xl"
          >
            {loading && suggestions.length === 0 && (
              <div className="px-4 py-3 text-sm text-ink-500 flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-brand-500 animate-pulse"></div>
                Searching...
              </div>
            )}
            {suggestions.map((s, i) => {
              const Icon = typeIcon[s.type] || Search
              const isActive = i === activeIndex
              return (
                <button
                  key={`${s.type}-${s.value}-${i}`}
                  onMouseEnter={() => setActiveIndex(i)}
                  onClick={() => handlePick(s)}
                  className={`w-full flex items-center gap-3 px-4 py-2.5 text-left transition-colors ${
                    isActive
                      ? 'bg-brand-50 dark:bg-brand-900/30'
                      : 'hover:bg-ink-50 dark:hover:bg-ink-800/50'
                  }`}
                  type="button"
                >
                  <Icon size={15} className={typeColor[s.type] || 'text-ink-400'}/>
                  <span className="flex-1 text-sm font-medium">
                    {highlightMatch(s.value, value)}
                  </span>
                  <span className="text-xs text-ink-400">
                    {s.category || typeLabel[s.type] || ''}
                  </span>
                </button>
              )
            })}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Highlight the matched portion of the suggestion text
function highlightMatch(text, query) {
  if (!query) return text
  const q = query.trim().toLowerCase()
  const lower = text.toLowerCase()
  const idx = lower.indexOf(q)
  if (idx < 0) return text
  return (
    <>
      {text.slice(0, idx)}
      <span className="text-brand-600 dark:text-brand-400 font-semibold">
        {text.slice(idx, idx + q.length)}
      </span>
      {text.slice(idx + q.length)}
    </>
  )
}
