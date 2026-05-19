import { motion } from 'framer-motion'

export function SkeletonCard() {
  return (
    <div className="card p-5 relative overflow-hidden">
      <div className="shimmer h-5 rounded w-3/4 mb-3"></div>
      <div className="shimmer h-4 rounded w-1/2 mb-4"></div>
      <div className="flex gap-2 mb-3">
        <div className="shimmer h-6 rounded w-16"></div>
        <div className="shimmer h-6 rounded w-20"></div>
        <div className="shimmer h-6 rounded w-14"></div>
      </div>
      <div className="shimmer h-9 rounded w-full mt-4"></div>
    </div>
  )
}

export function SkeletonBar({ width = 'w-full', height = 'h-4' }) {
  return <div className={`shimmer rounded ${width} ${height}`}></div>
}

export function SkeletonGrid({ count = 6, Component = SkeletonCard }) {
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {Array.from({ length: count }).map((_, i) => <Component key={i} />)}
    </div>
  )
}

/**
 * RadarLoader - signature loading state with rotating radar sweep.
 * Use for primary loading states to match the brand.
 */
export function RadarLoader({ label = 'Scanning the job market...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12 gap-4">
      <div className="relative w-24 h-24">
        {/* outer ring */}
        <div className="absolute inset-0 rounded-full border-2 border-brand-200 dark:border-brand-900/50"></div>
        {/* inner ring */}
        <div className="absolute inset-3 rounded-full border-2 border-brand-300 dark:border-brand-800/50"></div>
        {/* center dot */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-brand-500"></div>
        {/* pulse */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-brand-500 pulse-ring"></div>
        {/* rotating sweep */}
        <motion.div
          className="absolute inset-0"
          animate={{ rotate: 360 }}
          transition={{ duration: 1.8, ease: 'linear', repeat: Infinity }}
        >
          <div
            className="absolute top-1/2 left-1/2 w-1/2 h-[3px] origin-left"
            style={{
              background: 'linear-gradient(90deg, rgba(99,102,241,0) 0%, rgba(99,102,241,0.6) 70%, rgba(167,139,250,1) 100%)',
            }}
          />
        </motion.div>
      </div>
      <motion.p
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 1.5, repeat: Infinity }}
        className="text-sm text-ink-500"
      >
        {label}
      </motion.p>
    </div>
  )
}
