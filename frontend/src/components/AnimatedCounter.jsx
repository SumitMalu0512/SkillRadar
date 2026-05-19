import { useEffect, useState, useRef } from 'react'
import { motion, useInView } from 'framer-motion'

/**
 * AnimatedCounter - counts from 0 to target when scrolled into view.
 * Props:
 *   value: final number
 *   duration: ms (default 1500)
 *   suffix: e.g. "%", "+", "k"
 *   prefix: e.g. "$"
 */
export default function AnimatedCounter({
  value,
  duration = 1500,
  suffix = '',
  prefix = '',
  className = '',
  decimals = 0,
}) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-50px' })
  const [display, setDisplay] = useState(0)

  useEffect(() => {
    if (!inView) return
    const start = performance.now()
    const from = 0
    const to = Number(value) || 0

    let raf
    const tick = (now) => {
      const elapsed = now - start
      const t = Math.min(elapsed / duration, 1)
      // ease-out cubic for a nice slow-down at the end
      const eased = 1 - Math.pow(1 - t, 3)
      setDisplay(from + (to - from) * eased)
      if (t < 1) raf = requestAnimationFrame(tick)
    }
    raf = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(raf)
  }, [inView, value, duration])

  const formatted = decimals > 0
    ? display.toFixed(decimals)
    : Math.round(display).toLocaleString()

  return (
    <motion.span
      ref={ref}
      initial={{ opacity: 0, y: 10 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.4 }}
      className={className}
    >
      {prefix}{formatted}{suffix}
    </motion.span>
  )
}
