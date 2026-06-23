<template>
  <Transition name="loader-fade">
    <div v-if="visible" class="loading-screen">
      <div class="loader-inner">
        <!-- The Ring Forming Animation -->
        <div class="ring-stage">
          <svg
            class="ring-svg"
            viewBox="0 0 200 200"
            xmlns="http://www.w3.org/2000/svg"
          >
            <!-- Outer ring — the main one, drawn first -->
            <circle
              class="ring ring-outer"
              cx="100"
              cy="100"
              r="78"
              fill="none"
              stroke="url(#goldGradient)"
              stroke-width="1.2"
              stroke-linecap="round"
            />

            <!-- Inner ring — subtle, drawn slightly after -->
            <circle
              class="ring ring-inner"
              cx="100"
              cy="100"
              r="70"
              fill="none"
              stroke="#deba4e"
              stroke-width="0.4"
              stroke-linecap="round"
              opacity="0.5"
            />

            <!-- Gold gradient definition -->
            <defs>
              <linearGradient id="goldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#e8c9a0" />
                <stop offset="50%" stop-color="#deba4e" />
                <stop offset="100%" stop-color="#b8865c" />
              </linearGradient>
            </defs>
          </svg>

          <!-- Logo inside the ring -->
          <div
            ref="logoRef"
            class="ring-logo"
            :class="{ 'is-visible': textVisible }"
            v-html="logoSvg"
          ></div>

          <!-- Spark on ring close -->
          <div class="spark" :class="{ 'is-active': sparkActive }"></div>
        </div>

        <!-- Progress bar -->
        <div class="loader-progress">
          <div class="loader-progress-bar" :style="{ width: progress + '%' }"></div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import logoSvg from '../../RingsLogo.svg?raw'

const logoRef = ref(null)
const RING_DRAW_MS = 1800
const TEXT_DELAY_MS = 1500
const SPARK_DELAY_MS = 1800
const HOLD_MS = 700
const TOTAL_MS = TEXT_DELAY_MS + 800 + HOLD_MS

const visible = ref(true)
const progress = ref(0)
const textVisible = ref(false)
const sparkActive = ref(false)

let prevScrollRestoration = null
let prevBodyOverflow = null
let prevHtmlOverflow = null

onMounted(() => {
  if ('scrollRestoration' in history) {
    prevScrollRestoration = history.scrollRestoration
    history.scrollRestoration = 'manual'
  }
  window.scrollTo(0, 0)

  prevBodyOverflow = document.body.style.overflow
  prevHtmlOverflow = document.documentElement.style.overflow
  document.body.style.overflow = 'hidden'
  document.documentElement.style.overflow = 'hidden'

  const start = performance.now()
  const tick = (now) => {
    const elapsed = now - start
    progress.value = Math.min(100, (elapsed / TOTAL_MS) * 100)
    if (elapsed < TOTAL_MS) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)

  setTimeout(() => { sparkActive.value = true }, SPARK_DELAY_MS)
  setTimeout(() => { textVisible.value = true }, TEXT_DELAY_MS)

  setTimeout(() => {
    visible.value = false
    document.body.style.overflow = prevBodyOverflow ?? ''
    document.documentElement.style.overflow = prevHtmlOverflow ?? ''
    window.scrollTo(0, 0)
    if ('scrollRestoration' in history && prevScrollRestoration) {
      history.scrollRestoration = prevScrollRestoration
    }
  }, TOTAL_MS + 200)
})

onBeforeUnmount(() => {
  document.body.style.overflow = prevBodyOverflow ?? ''
  document.documentElement.style.overflow = prevHtmlOverflow ?? ''
})
</script>

<style scoped>
.loading-screen {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background:
    radial-gradient(ellipse at 50% 45%, #0d1f1a 0%, #060d0b 70%, #030605 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

/* Subtle radial gold glow + green base tint */
.loading-screen::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 50% 45%, rgba(222, 186, 78, 0.08), transparent 50%);
  pointer-events: none;
}

.loader-inner {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4rem;
  width: min(420px, 70vw);
  z-index: 1;
}

/* === RING STAGE === */
.ring-stage {
  position: relative;
  width: min(340px, 60vw);
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.ring-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
  transform: rotate(-90deg); /* start drawing from top */
}

/* Stroke draw — circumference = 2πr ≈ 490 for r=78 */
.ring-outer {
  stroke-dasharray: 490;
  stroke-dashoffset: 490;
  animation: ringDraw 1800ms cubic-bezier(0.65, 0, 0.35, 1) forwards;
  filter: drop-shadow(0 0 4px rgba(222, 186, 78, 0.4));
}

/* circumference for r=70 ≈ 440 */
.ring-inner {
  stroke-dasharray: 440;
  stroke-dashoffset: 440;
  animation: ringDraw 1800ms cubic-bezier(0.65, 0, 0.35, 1) 150ms forwards;
}

@keyframes ringDraw {
  to {
    stroke-dashoffset: 0;
  }
}

/* === SPARK on ring close — diffuse glow, no hard center === */
.spark {
  position: absolute;
  top: 8%;
  left: 50%;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: radial-gradient(
    circle,
    rgba(255, 240, 200, 0.5) 0%,
    rgba(222, 186, 78, 0.25) 40%,
    transparent 70%
  );
  filter: blur(8px);
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  pointer-events: none;
  mix-blend-mode: screen;
}

.spark.is-active {
  animation: sparkFlash 900ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

@keyframes sparkFlash {
  0% {
    transform: translate(-50%, -50%) scale(0.3);
    opacity: 0;
  }
  30% {
    transform: translate(-50%, -50%) scale(1.2);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.6);
    opacity: 0;
  }
}

/* === LOGO INSIDE THE RING === */
.ring-logo {
  position: relative;
  width: 62%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.92);
  transition:
    opacity 900ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 900ms cubic-bezier(0.22, 1, 0.36, 1);
  filter: drop-shadow(0 0 12px rgba(222, 186, 78, 0.2));
}

.ring-logo.is-visible {
  opacity: 1;
  transform: scale(1);
}

.ring-logo :deep(svg) {
  width: 100%;
  height: auto;
  display: block;
}

/* Variant 9: Platinum + Gold (inverted accents) */
/* Previously gold (.st0) → platinum/silver */
.ring-logo :deep(.st0) {
  fill: #d4d8de !important;
}

/* Previously dark-green (.st1) → warm gold */
.ring-logo :deep(.st1) {
  fill: #deba4e !important;
}

.ring-logo :deep(rect.st1) {
  fill: #deba4e !important;
}


/* === PROGRESS BAR === */
.loader-progress {
  width: 100%;
  height: 3px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 0 8px rgba(222, 186, 78, 0.2) inset;
}

.loader-progress-bar {
  height: 100%;
  background: linear-gradient(90deg,
    #deba4e 0%,
    #e8c9a0 50%,
    #10b981 100%
  );
  box-shadow: 0 0 16px #deba4e, 0 0 8px rgba(16, 185, 129, 0.6);
  border-radius: 999px;
  position: relative;
  will-change: width;
}

.loader-progress-bar::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  border-radius: 999px;
  animation: progressShine 2s infinite;
}

@keyframes progressShine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* === EXIT === */
.loader-fade-leave-active {
  transition: transform 900ms cubic-bezier(0.76, 0, 0.24, 1);
}

.loader-fade-leave-to {
  transform: translateY(-100%);
}
</style>
