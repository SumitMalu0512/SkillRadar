import { motion } from 'framer-motion'

/**
 * Animated Radar - signature SkillRadar visual element.
 * Pure SVG with framer-motion animations. Auto-scales, light/dark aware.
 *
 * Props:
 *   size: pixel dimension (default 480)
 *   className: positioning classes
 */
export default function AnimatedRadar({ size = 480, className = '' }) {
  return (
    <div
      className={`pointer-events-none select-none ${className}`}
      style={{ width: size, height: size }}
      aria-hidden="true"
    >
      <svg viewBox="0 0 480 480" className="w-full h-full">
        <defs>
          {/* radar sweep gradient */}
          <linearGradient id="sweepGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%"   stopColor="rgba(99,102,241,0)"/>
            <stop offset="60%"  stopColor="rgba(99,102,241,0.25)"/>
            <stop offset="100%" stopColor="rgba(167,139,250,0.55)"/>
          </linearGradient>

          <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%"   stopColor="rgba(99,102,241,0.5)"/>
            <stop offset="40%"  stopColor="rgba(99,102,241,0.15)"/>
            <stop offset="100%" stopColor="rgba(99,102,241,0)"/>
          </radialGradient>

          {/* Soft outer glow filter */}
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <g transform="translate(240 240)">
          {/* Center glow */}
          <circle cx="0" cy="0" r="220" fill="url(#centerGlow)"/>

          {/* Concentric rings */}
          {[80, 140, 200].map((r, i) => (
            <motion.circle
              key={r}
              cx="0" cy="0" r={r}
              fill="none"
              stroke="currentColor"
              strokeWidth="0.8"
              className="text-brand-500/30"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: i * 0.15, duration: 0.6 }}
            />
          ))}

          {/* Crosshairs */}
          <line x1="-220" y1="0" x2="220" y2="0" stroke="currentColor" strokeWidth="0.5" strokeDasharray="2 4" className="text-brand-500/20"/>
          <line x1="0" y1="-220" x2="0" y2="220" stroke="currentColor" strokeWidth="0.5" strokeDasharray="2 4" className="text-brand-500/20"/>

          {/* Rotating sweep arm */}
          <motion.g
            animate={{ rotate: 360 }}
            transition={{ duration: 6, ease: 'linear', repeat: Infinity }}
          >
            <path
              d="M0 0 L220 0 A220 220 0 0 0 155 -155 Z"
              fill="url(#sweepGrad)"
            />
            <line x1="0" y1="0" x2="220" y2="0" stroke="rgb(167,139,250)" strokeWidth="1.5"/>
          </motion.g>

          {/* Skill blip dots - simulate detected skills on the radar */}
          {[
            { x: 80, y: -100, label: 'Python', delay: 0 },
            { x: -120, y: -60, label: 'React', delay: 0.8 },
            { x: 140, y: 60, label: 'AWS', delay: 1.5 },
            { x: -80, y: 120, label: 'AI/ML', delay: 2.2 },
            { x: 50, y: 150, label: 'Docker', delay: 2.9 },
            { x: -160, y: 30, label: 'Java', delay: 3.6 },
            { x: 170, y: -40, label: 'SQL', delay: 4.3 },
          ].map((blip) => (
            <Blip key={blip.label} {...blip}/>
          ))}

          {/* Center pulse */}
          <circle cx="0" cy="0" r="6" fill="rgb(99,102,241)" filter="url(#glow)"/>
          <motion.circle
            cx="0" cy="0" r="6"
            fill="none"
            stroke="rgb(99,102,241)"
            strokeWidth="1.5"
            animate={{ r: [6, 30], opacity: [0.8, 0] }}
            transition={{ duration: 2.5, repeat: Infinity, ease: 'easeOut' }}
          />
        </g>
      </svg>
    </div>
  )
}

function Blip({ x, y, label, delay }) {
  return (
    <motion.g
      initial={{ opacity: 0 }}
      animate={{ opacity: [0, 1, 1, 0.3, 1] }}
      transition={{
        duration: 6,
        repeat: Infinity,
        delay,
        times: [0, 0.05, 0.4, 0.7, 1],
      }}
    >
      {/* glow */}
      <circle cx={x} cy={y} r="10" fill="rgba(245,158,11,0.15)" filter="url(#glow)"/>
      {/* dot */}
      <circle cx={x} cy={y} r="3.5" fill="rgb(245,158,11)"/>
      {/* label */}
      <text
        x={x + 10}
        y={y + 3}
        fontSize="10"
        fontWeight="600"
        className="fill-ink-700 dark:fill-ink-200"
        style={{ fontFamily: 'Inter, sans-serif' }}
      >
        {label}
      </text>
    </motion.g>
  )
}
