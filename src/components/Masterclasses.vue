<template>
  <section id="masterclass">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Шаг за шагом</span>
        <h2 class="section-title heading-font">Ювелирный мастер-класс: кольца своими руками</h2>
        <div class="separator"></div>
      </div>
    </div>

    <!-- Desktop: scroll-driven timeline -->
    <div class="tl-wrapper tl-desktop" ref="wrapperRef">
      <div class="tl-sticky">

        <!-- Left: step labels -->
        <nav class="tl-labels">
          <div
            v-for="(step, i) in steps"
            :key="i"
            :class="['tl-label', { 'is-active': activeStep === i, 'is-past': i < activeStep }]"
          >
            <span class="tl-label-num heading-font">{{ step.number }}</span>
            <span class="tl-label-title heading-font">{{ step.title }}</span>
          </div>
        </nav>

        <!-- Center: timeline line -->
        <div class="tl-line-wrap">
          <div class="tl-track"></div>
          <div class="tl-fill" :style="{ height: fillPercent + '%' }"></div>
          <div class="tl-glow-dot" :style="{ top: 'calc(' + fillPercent + '% - 8px)' }"></div>
          <div
            v-for="(_, i) in steps"
            :key="i"
            :class="['tl-node', { 'is-active': activeStep === i, 'is-past': i <= activeStep }]"
            :style="{ top: (i / (steps.length - 1)) * 100 + '%' }"
          ></div>
        </div>

        <!-- Right: active step card -->
        <div class="tl-card-wrap">
          <Transition name="tl-rise">
            <div :key="activeStep" class="tl-card glass-card">
              <div class="tl-card-img-wrap">
                <img :src="steps[activeStep].image" :alt="steps[activeStep].title" class="tl-card-img" width="1200" height="1800" loading="lazy" decoding="async">
              </div>
              <div class="tl-card-body">
                <div class="tl-card-num" :class="'tl-num-font-' + activeStep">{{ steps[activeStep].number }}</div>
                <h3 class="tl-card-title heading-font">{{ steps[activeStep].title }}</h3>
                <p class="tl-card-desc font-light">{{ steps[activeStep].desc }}</p>
              </div>
            </div>
          </Transition>
        </div>

      </div>
    </div>

    <!-- Mobile: stacked cards -->
    <div class="container tl-mobile">
      <div
        v-for="(step, i) in steps"
        :key="i"
        class="tl-mobile-card glass-card"
        data-reveal
        :data-reveal-delay="(i % 3) + 1"
      >
        <div class="tl-mobile-img-wrap">
          <img :src="step.image" :alt="step.title" class="tl-mobile-img" width="1200" height="1800" loading="lazy" decoding="async">
        </div>
        <div class="tl-mobile-body">
          <div class="tl-mobile-num heading-font" :class="'tl-num-font-' + i">{{ step.number }}</div>
          <h3 class="tl-mobile-title heading-font">{{ step.title }}</h3>
          <p class="tl-mobile-desc font-light">{{ step.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import imgStep1 from '../assets/Step_1.webp'
import imgStep2 from '../assets/Step_2.webp'
import imgStep3 from '../assets/Step_3.webp'
import imgStep4 from '../assets/Step_4.webp'
import imgStep5 from '../assets/Step_5.webp'

const wrapperRef = ref(null)
const activeStep = ref(0)
const fillPercent = ref(0)
let rafId = null

const steps = [
  {
    number: '01',
    title: 'Плавка и создание сплава',
    desc: 'Вы получаете золото высшей 999,9 пробы и самостоятельно выбираете цвет будущих обручальных колец. Вместе с ювелиром взвешиваете металл и лигатуру, плавите до состояния раскалённой лавы и выливаете в изложницу — так рождается ваш личный слиток.',
    image: imgStep1
  },
  {
    number: '02',
    title: 'Раскатка и подготовка заготовок',
    desc: 'Слиток раскатываете на профессиональных ювелирных вальцах, превращая его в тонкую полосу. Заготовки обжигаются для податливости, затем распиливаются на две части — для мужского и женского кольца.',
    image: imgStep2
  },
  {
    number: '03',
    title: 'Формовка колец',
    desc: 'Каждую заготовку сгибаете в кольцо и запаиваете шов ювелирным припоем. Один из самых волнующих моментов на мастер-классе — металл обретает форму будущих обручальных колец прямо в ваших руках.',
    image: imgStep3
  },
  {
    number: '04',
    title: 'Выравнивание и шлифовка',
    desc: 'Молотком выравниваете форму кольца, придавая идеальную геометрию. Затем шлифуете боковые стороны ювелирной шкуркой и полируете внутреннюю поверхность бормашиной.',
    image: imgStep4
  },
  {
    number: '05',
    title: 'Финальная полировка',
    desc: 'На большой полировальной машине кольца приобретают зеркальный блеск. Завершающий штрих — ультразвуковая ванна. Вы держите в руках пару обручальных колец, созданных своими руками в студии Rings Atelier.',
    image: imgStep5
  }
]

const update = () => {
  if (!wrapperRef.value) return
  const rect = wrapperRef.value.getBoundingClientRect()
  const vh = window.innerHeight
  const stepHeight = vh * 0.6
  const scrolled = Math.max(0, -rect.top)

  // Плавный прогресс-бар (0-100%)
  const totalScroll = stepHeight * (steps.length - 1)
  fillPercent.value = Math.min(100, (scrolled / totalScroll) * 100)

  // Контент меняется дискретно при достижении каждого шага
  activeStep.value = Math.min(steps.length - 1, Math.floor(scrolled / stepHeight))
}

const onScroll = () => {
  if (rafId) return
  rafId = requestAnimationFrame(() => {
    rafId = null
    update()
  })
}

onMounted(() => {
  update()
  window.addEventListener('scroll', onScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  if (rafId) cancelAnimationFrame(rafId)
})
</script>
