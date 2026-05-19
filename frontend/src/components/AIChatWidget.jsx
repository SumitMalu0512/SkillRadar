import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MessageCircle, X, Send, Sparkles, Loader2, Bot, User } from 'lucide-react'
import { aiAPI } from '../lib/api'

const SUGGESTIONS = [
  "What skills are trending right now?",
  "What's growing in the job market?",
  "Which roles cluster together?",
  "Compare Python vs Java demand",
]

export default function AIChatWidget() {
  const [open, setOpen] = useState(false)
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm SkillRadar's AI assistant. I have access to live job market data and can answer questions about skills, trends, roles, and forecasts. What would you like to know?",
    },
  ])
  const [loading, setLoading] = useState(false)
  const scrollRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, loading])

  useEffect(() => {
    if (open) inputRef.current?.focus()
  }, [open])

  const send = async (text) => {
    const message = (text || input).trim()
    if (!message || loading) return

    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setLoading(true)

    try {
      // pass last few messages as history for context
      const history = messages.slice(-6).filter(m => m.role !== 'system')
      const data = await aiAPI.chat(message, history)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.reply || 'I had trouble responding to that.',
        source: data.source,
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I could not reach the AI service. Please try again in a moment.',
        error: true,
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <>
      {/* Floating button */}
      <AnimatePresence>
        {!open && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 20 }}
            onClick={() => setOpen(true)}
            className="fixed bottom-6 right-6 z-40 w-14 h-14 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white shadow-lg shadow-brand-600/40 hover:shadow-xl hover:shadow-brand-600/50 hover:scale-110 transition-all flex items-center justify-center group"
            aria-label="Open AI Chat"
          >
            <MessageCircle size={22}/>
            <span className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-accent-500 flex items-center justify-center">
              <Sparkles size={10} className="text-white"/>
            </span>
            <span className="absolute right-full mr-3 px-3 py-1.5 rounded-lg bg-ink-900 dark:bg-ink-100 text-white dark:text-ink-900 text-xs font-medium whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
              Ask AI
            </span>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat panel */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 350, damping: 28 }}
            className="fixed bottom-6 right-6 z-40 w-[min(420px,calc(100vw-3rem))] h-[min(620px,calc(100vh-3rem))] card flex flex-col shadow-2xl overflow-hidden"
          >
            {/* Header */}
            <div className="flex-shrink-0 p-4 border-b border-ink-200 dark:border-ink-800 bg-gradient-to-br from-brand-50 to-transparent dark:from-brand-900/20 dark:to-transparent">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-brand-700 flex items-center justify-center text-white">
                  <Sparkles size={18}/>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-display font-bold">SkillRadar AI</h3>
                  <p className="text-xs text-ink-500 flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                    Connected to live market data
                  </p>
                </div>
                <button
                  onClick={() => setOpen(false)}
                  className="p-2 hover:bg-ink-100 dark:hover:bg-ink-800 rounded-lg transition-colors"
                  aria-label="Close"
                >
                  <X size={18}/>
                </button>
              </div>
            </div>

            {/* Messages */}
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((m, i) => (
                <Message key={i} message={m}/>
              ))}
              {loading && <TypingIndicator/>}

              {/* Suggestion chips - only show after initial greeting */}
              {messages.length === 1 && !loading && (
                <div className="mt-4 space-y-2">
                  <p className="text-xs text-ink-500 px-1">Try asking:</p>
                  {SUGGESTIONS.map(s => (
                    <button
                      key={s}
                      onClick={() => send(s)}
                      className="block w-full text-left text-sm px-3 py-2 rounded-lg border border-ink-200 dark:border-ink-700 hover:border-brand-500 hover:bg-brand-50 dark:hover:bg-brand-900/20 transition-colors"
                    >
                      {s}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Input */}
            <div className="flex-shrink-0 p-3 border-t border-ink-200 dark:border-ink-800">
              <div className="flex gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about skills, trends, jobs..."
                  className="input-field !py-2 text-sm flex-1"
                  disabled={loading}
                />
                <button
                  onClick={() => send()}
                  disabled={loading || !input.trim()}
                  className="btn-primary px-3"
                  aria-label="Send"
                >
                  {loading ? <Loader2 size={16} className="animate-spin"/> : <Send size={16}/>}
                </button>
              </div>
              <p className="text-xs text-ink-400 mt-2 text-center">
                Powered by Llama 3 via Groq · Responses based on live data
              </p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

function Message({ message }) {
  const isUser = message.role === 'user'
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex gap-2 ${isUser ? 'flex-row-reverse' : ''}`}
    >
      <div className={`flex-shrink-0 w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold ${
        isUser
          ? 'bg-ink-200 dark:bg-ink-700'
          : 'bg-gradient-to-br from-brand-500 to-brand-700 text-white'
      }`}>
        {isUser ? <User size={14}/> : <Bot size={14}/>}
      </div>
      <div className={`max-w-[80%] px-3 py-2 rounded-2xl text-sm leading-relaxed ${
        isUser
          ? 'bg-brand-600 text-white rounded-tr-md'
          : message.error
            ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 rounded-tl-md'
            : 'bg-ink-100 dark:bg-ink-800 text-ink-900 dark:text-ink-100 rounded-tl-md'
      }`}>
        <MessageContent text={message.content}/>
        {message.source === 'fallback' && !isUser && (
          <p className="text-[10px] mt-2 opacity-60">(fallback mode - set GROQ_API_KEY for AI responses)</p>
        )}
      </div>
    </motion.div>
  )
}

function MessageContent({ text }) {
  // Render basic markdown: bold, italic, code
  if (!text) return null
  // Convert **bold** and *italic* and `code`
  const parts = []
  const regex = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\n)/g
  let lastIndex = 0
  let match
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index))
    }
    const m = match[0]
    if (m === '\n') {
      parts.push(<br key={`br-${match.index}`}/>)
    } else if (m.startsWith('**')) {
      parts.push(<strong key={`b-${match.index}`}>{m.slice(2, -2)}</strong>)
    } else if (m.startsWith('*')) {
      parts.push(<em key={`i-${match.index}`}>{m.slice(1, -1)}</em>)
    } else if (m.startsWith('`')) {
      parts.push(<code key={`c-${match.index}`} className="px-1 py-0.5 rounded bg-black/10 dark:bg-white/10 text-xs font-mono">{m.slice(1, -1)}</code>)
    }
    lastIndex = match.index + m.length
  }
  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex))
  }
  return <>{parts}</>
}

function TypingIndicator() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-2">
      <div className="w-7 h-7 rounded-full bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center">
        <Bot size={14}/>
      </div>
      <div className="px-3 py-3 rounded-2xl rounded-tl-md bg-ink-100 dark:bg-ink-800 flex items-center gap-1.5">
        {[0, 1, 2].map(i => (
          <motion.div
            key={i}
            animate={{ y: [0, -3, 0] }}
            transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
            className="w-1.5 h-1.5 rounded-full bg-ink-400 dark:bg-ink-500"
          />
        ))}
      </div>
    </motion.div>
  )
}
