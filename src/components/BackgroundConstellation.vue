<template>
  <canvas
    ref="canvasRef"
    class="constellation-canvas"
    aria-hidden="true"
  ></canvas>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const canvasRef = ref(null)

// Tunables
const PARTICLE_DENSITY = 0.00008 // particles per pixel of viewport area
const MAX_LINK_DISTANCE = 140    // px — link between particles closer than this
const MOUSE_RADIUS = 180         // px — particles attracted/linked to cursor
const PARTICLE_SPEED = 0.18      // px per frame
const PARTICLE_COLOR = [222, 186, 78] // gold
const PARTICLE_SIZE = 1.2        // base radius

let ctx = null
let particles = []
let mouse = { x: -9999, y: -9999, active: false }
let rafId = null
let dpr = 1

function resize() {
  const canvas = canvasRef.value
  if (!canvas) return
  dpr = Math.min(window.devicePixelRatio || 1, 2)
  canvas.width = window.innerWidth * dpr
  canvas.height = window.innerHeight * dpr
  canvas.style.width = window.innerWidth + 'px'
  canvas.style.height = window.innerHeight + 'px'
  ctx.setTransform(1, 0, 0, 1, 0, 0)
  ctx.scale(dpr, dpr)
  spawnParticles()
}

function spawnParticles() {
  const w = window.innerWidth
  const h = window.innerHeight
  const target = Math.max(40, Math.min(120, Math.round(w * h * PARTICLE_DENSITY)))
  particles = []
  for (let i = 0; i < target; i++) {
    const baseVx = (Math.random() - 0.5) * PARTICLE_SPEED
    const baseVy = (Math.random() - 0.5) * PARTICLE_SPEED
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      vx: baseVx,
      vy: baseVy,
      baseVx,
      baseVy,
      r: PARTICLE_SIZE + Math.random() * 0.8,
      twinkle: Math.random() * Math.PI * 2
    })
  }
}

function step() {
  const w = window.innerWidth
  const h = window.innerHeight
  ctx.clearRect(0, 0, w, h)

  // Update + draw particles
  for (let i = 0; i < particles.length; i++) {
    const p = particles[i]

    // Damping — gently return to base drift speed
    p.vx = p.vx * 0.985 + p.baseVx * 0.015
    p.vy = p.vy * 0.985 + p.baseVy * 0.015

    p.x += p.vx
    p.y += p.vy
    p.twinkle += 0.02

    // Wrap around edges
    if (p.x < -10) p.x = w + 10
    if (p.x > w + 10) p.x = -10
    if (p.y < -10) p.y = h + 10
    if (p.y > h + 10) p.y = -10

    const twinkleAlpha = 0.45 + Math.sin(p.twinkle) * 0.25
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(${PARTICLE_COLOR[0]}, ${PARTICLE_COLOR[1]}, ${PARTICLE_COLOR[2]}, ${twinkleAlpha})`
    ctx.fill()
  }

  // Draw links between close particles
  for (let i = 0; i < particles.length; i++) {
    const p1 = particles[i]
    for (let j = i + 1; j < particles.length; j++) {
      const p2 = particles[j]
      const dx = p1.x - p2.x
      const dy = p1.y - p2.y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < MAX_LINK_DISTANCE) {
        const alpha = (1 - dist / MAX_LINK_DISTANCE) * 0.25
        ctx.beginPath()
        ctx.moveTo(p1.x, p1.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = `rgba(${PARTICLE_COLOR[0]}, ${PARTICLE_COLOR[1]}, ${PARTICLE_COLOR[2]}, ${alpha})`
        ctx.lineWidth = 0.6
        ctx.stroke()
      }
    }
  }

  // Cursor-reactive links
  if (mouse.active) {
    for (let i = 0; i < particles.length; i++) {
      const p = particles[i]
      const dx = p.x - mouse.x
      const dy = p.y - mouse.y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < MOUSE_RADIUS) {
        const alpha = (1 - dist / MOUSE_RADIUS) * 0.55
        // Subtle pull toward cursor
        p.vx += (mouse.x - p.x) * 0.00006
        p.vy += (mouse.y - p.y) * 0.00006
        // Cap velocity
        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy)
        if (speed > PARTICLE_SPEED * 2) {
          p.vx = (p.vx / speed) * PARTICLE_SPEED * 2
          p.vy = (p.vy / speed) * PARTICLE_SPEED * 2
        }
        ctx.beginPath()
        ctx.moveTo(p.x, p.y)
        ctx.lineTo(mouse.x, mouse.y)
        ctx.strokeStyle = `rgba(232, 201, 160, ${alpha})`
        ctx.lineWidth = 0.8
        ctx.stroke()
      }
    }
  }

  rafId = requestAnimationFrame(step)
}

function onMouseMove(e) {
  mouse.x = e.clientX
  mouse.y = e.clientY
  mouse.active = true
}

function onMouseLeave() {
  mouse.active = false
}

function onTouchMove(e) {
  if (e.touches.length > 0) {
    mouse.x = e.touches[0].clientX
    mouse.y = e.touches[0].clientY
    mouse.active = true
  }
}

function onTouchEnd() {
  mouse.active = false
}

onMounted(() => {
  const canvas = canvasRef.value
  ctx = canvas.getContext('2d')
  resize()
  window.addEventListener('resize', resize)
  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.addEventListener('mouseleave', onMouseLeave, { passive: true })
  window.addEventListener('touchmove', onTouchMove, { passive: true })
  window.addEventListener('touchend', onTouchEnd, { passive: true })
  step()
})

onBeforeUnmount(() => {
  if (rafId) cancelAnimationFrame(rafId)
  window.removeEventListener('resize', resize)
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseleave', onMouseLeave)
  window.removeEventListener('touchmove', onTouchMove)
  window.removeEventListener('touchend', onTouchEnd)
})
</script>

<style scoped>
.constellation-canvas {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  pointer-events: none;
  z-index: 0;
  opacity: 0.85;
}
</style>
