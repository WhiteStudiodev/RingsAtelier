<template>
  <section class="clients-section">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Наши гости</span>
        <h2 class="section-title heading-font">Свадебные кольца, созданные на мастер-классе</h2>
        <div class="separator"></div>
      </div>
      
      <div class="carousel-wrapper" data-reveal data-reveal-delay="1">
        <button
          class="carousel-nav prev"
          @click="scrollPrev"
          :disabled="atStart"
          aria-label="Предыдущий слайд"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <div class="carousel-container" ref="containerRef">
          <div class="carousel-track" ref="trackRef">
            <div 
              v-for="(item, index) in realItems" 
              :key="`client-${index}`" 
              class="carousel-item"
            >
              <div class="glass-card client-card">
                <img :src="item.src" :alt="`Фото гостя ${index + 1}`" loading="lazy" decoding="async" width="600" height="800">
                <div class="client-overlay">
                  <span class="client-tag">#ringsatelier</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          class="carousel-nav next"
          @click="scrollNext"
          :disabled="atEnd"
          aria-label="Следующий слайд"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const clientPhotos = [
  '/clients/DSC05961.webp',
  '/clients/DSC06119.webp',
  '/clients/DSC06935.webp',
  '/clients/DSC07096.webp',
  '/clients/DSC07156.webp',
  '/clients/DSC07442.webp',
  '/clients/DSC07626.webp',
  '/clients/DSC07670.webp',
  '/clients/IMG_2172.webp',
  '/clients/IMG_2735.webp',
  '/clients/IMG_2839.webp',
  '/clients/IMG_2924.webp'
]

const realItems = clientPhotos.map((src, i) => ({ id: i, src }))

const containerRef = ref(null)
const trackRef = ref(null)
const cardWidth = ref(280)
const cardGap = ref(32)
const scrollLeft = ref(0)
const maxScroll = ref(0)

const cardStep = computed(() => cardWidth.value + cardGap.value)

const updateDimensions = () => {
  if (trackRef.value) {
    const styles = getComputedStyle(trackRef.value)
    const widthValue = styles.getPropertyValue('--carousel-card-width').trim()
    const gapValue = styles.getPropertyValue('--carousel-gap').trim()
    if (widthValue) cardWidth.value = parseFloat(widthValue)
    if (gapValue) cardGap.value = parseFloat(gapValue)
  }
  if (containerRef.value) {
    scrollLeft.value = containerRef.value.scrollLeft
    maxScroll.value = containerRef.value.scrollWidth - containerRef.value.clientWidth
  }
}

const onScroll = () => {
  if (containerRef.value) {
    scrollLeft.value = containerRef.value.scrollLeft
    maxScroll.value = containerRef.value.scrollWidth - containerRef.value.clientWidth
  }
}

const atStart = computed(() => scrollLeft.value <= 5)
const atEnd = computed(() => maxScroll.value <= 0 || scrollLeft.value >= maxScroll.value - 5)

const scrollNext = () => {
  if (containerRef.value) {
    containerRef.value.scrollBy({ left: cardStep.value, behavior: 'smooth' })
  }
}

const scrollPrev = () => {
  if (containerRef.value) {
    containerRef.value.scrollBy({ left: -cardStep.value, behavior: 'smooth' })
  }
}

onMounted(() => {
  updateDimensions()
  window.addEventListener('resize', updateDimensions)
  if (containerRef.value) {
    containerRef.value.addEventListener('scroll', onScroll, { passive: true })
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', updateDimensions)
  if (containerRef.value) {
    containerRef.value.removeEventListener('scroll', onScroll)
  }
})
</script>

<style scoped>
.clients-section {
  padding: 3rem 0;
  overflow: hidden;
}

.carousel-wrapper {
  display: flex;
  align-items: center;
  position: relative;
  margin-top: 3rem;
}

.carousel-container {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
  padding: 2rem 0;
  margin: -1rem 0;
  -webkit-mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
  mask-image: linear-gradient(to right, transparent, black 8%, black 92%, transparent);
}

.carousel-container::-webkit-scrollbar {
  display: none;
}

.carousel-track {
  --carousel-card-width: 280px;
  --carousel-gap: 2rem;
  display: flex;
  gap: var(--carousel-gap);
  width: max-content;
  padding: 0 1rem;
}

.carousel-item {
  width: var(--carousel-card-width);
  flex-shrink: 0;
  scroll-snap-align: start;
}

.client-card {
  aspect-ratio: 1;
  border-radius: 2rem;
  overflow: hidden;
  padding: 0.5rem;
}

.client-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1.5rem;
  transition: transform 0.5s ease;
}

@media (hover: hover) {
  .client-card:hover img {
    transform: scale(1.1);
  }
}

.client-overlay {
  position: absolute;
  bottom: 1.5rem;
  left: 1.5rem;
  z-index: 2;
}

.client-tag {
  background: rgba(2, 44, 34, 0.7);
  backdrop-filter: blur(4px);
  padding: 0.4rem 1rem;
  border-radius: 999px;
  font-size: 0.75rem;
  color: var(--color-accent);
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.carousel-nav {
  position: absolute;
  z-index: 10;
  background: rgba(2, 44, 34, 0.8);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: var(--color-accent);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.carousel-nav:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

@media (hover: hover) {
  .carousel-nav:hover:not(:disabled) {
    background: var(--color-accent);
    color: var(--color-bg);
    transform: scale(1.1);
  }
}

.carousel-nav.prev {
  left: -25px;
}

.carousel-nav.next {
  right: -25px;
}

@media (max-width: 768px) {
  .carousel-track {
    --carousel-card-width: 250px;
  }

  .carousel-nav.prev { left: 0; }
  .carousel-nav.next { right: 0; }
}
</style>
