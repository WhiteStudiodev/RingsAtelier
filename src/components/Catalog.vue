<template>
  <section id="products">
    <div class="container">
      <div class="section-header catalog-header" data-reveal>
        <h2 class="section-title heading-font catalog-title catalog-title-gold">Обручальные кольца на заказ в Спб</h2>
        <div class="separator"></div>
        <p class="catalog-lead">Примеры свадебных и обручальных колец, созданных на наших мастер-классах в Санкт-Петербурге. Вы всегда можете изменить дизайн, форму и фактуру, добавить гравировку или воплотить собственную идею в золоте, серебре или платине.</p>
      </div>

      <!-- Category filters -->
      <div class="category-filter" data-reveal>
        <!-- Desktop: inline row -->
        <div class="category-list">
          <button
            v-for="cat in categories"
            :key="cat"
            type="button"
            class="category-btn"
            :class="{ active: selectedCategory === cat }"
            @click="selectedCategory = cat"
          >{{ cat }}</button>
        </div>

        <!-- Mobile: burger dropdown -->
        <div class="category-mobile">
          <button
            type="button"
            class="category-burger"
            :class="{ open: isMobileMenuOpen }"
            aria-label="Категории"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
          >
            <span class="burger-line"></span>
            <span class="burger-line"></span>
            <span class="burger-line"></span>
            <span class="burger-label">{{ selectedCategory }}</span>
          </button>

          <Transition name="category-menu">
            <div v-if="isMobileMenuOpen" class="category-mobile-menu">
              <button
                v-for="cat in categories"
                :key="cat"
                type="button"
                class="category-mobile-item"
                :class="{ active: selectedCategory === cat }"
                @click="selectedCategory = cat; isMobileMenuOpen = false"
              >{{ cat }}</button>
            </div>
          </Transition>
        </div>
      </div>

      <div class="catalog-grid">
        <div
          v-for="(item, index) in visibleItems"
          :key="index"
          :class="['catalog-card', { bestseller: item.bestseller }]"
          data-reveal
          :data-reveal-delay="(index % 4) + 1"
          @mousemove="handleTilt"
          @mouseleave="resetTilt"
        >
          <div class="catalog-card-inner">
            <div class="catalog-img">
              <div v-if="item.bestseller" class="bestseller-badge">
                <span class="badge-dot"></span>
                Выбор мастеров
              </div>
              <img
                :src="item.images[0]"
                :alt="item.title"
                loading="lazy"
                decoding="async"
                width="1480"
                height="2048"
              >
              <div class="overlay">
                <a href="#" class="overlay-btn" @click.prevent="openModal(item)">
                  <span>Подробнее</span>
                  <svg class="overlay-btn-arrow" width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M1 7H13M13 7L7 1M13 7L7 13" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
                  </svg>
                </a>
              </div>
            </div>

            <div class="catalog-info">
              <div class="catalog-meta">
                <span class="catalog-index">{{ String(index + 1).padStart(2, '0') }}</span>
                <span class="catalog-material">{{ item.material }}</span>
              </div>
              <h4 class="product-title heading-font">{{ item.title }}</h4>
              <p class="product-desc font-light">{{ item.desc }}</p>
              <div class="catalog-divider"></div>
              <div class="product-price heading-font">
                <span class="price-from">от</span>
                {{ item.price }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="hasMore" class="show-more-wrap" data-reveal>
        <button class="show-more-btn" @click="showMore">
          <span>Показать ещё</span>
          <span class="show-more-count">{{ filteredItems.length - visibleCount }}</span>
        </button>
      </div>
    </div>

    <!-- Product Modal -->
    <Transition name="modal-fade">
      <div v-if="selectedProduct" class="modal-overlay" @click.self="closeModal">
        <Transition name="modal-content" appear>
          <div v-if="selectedProduct" class="modal-content">
            <button class="modal-close" @click="closeModal" aria-label="Закрыть">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 2L14 14M14 2L2 14" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
              </svg>
            </button>

            <div class="modal-image-wrapper">
              <div v-if="selectedProduct.bestseller" class="modal-bestseller">
                <span class="badge-dot"></span>
                Выбор мастеров
              </div>
              <img
                :src="selectedProduct.images[currentImage]"
                :alt="selectedProduct.title"
                class="modal-image"
                decoding="async"
                width="1480"
                height="2048"
              >

              <!-- Slider controls -->
              <template v-if="selectedProduct.images.length > 1">
                <button
                  type="button"
                  class="slider-arrow slider-arrow-prev"
                  aria-label="Предыдущее фото"
                  @click.stop="prevImage"
                >
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M12 4L6 10L12 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
                <button
                  type="button"
                  class="slider-arrow slider-arrow-next"
                  aria-label="Следующее фото"
                  @click.stop="nextImage"
                >
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M8 4L14 10L8 16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>

                <div class="slider-dots">
                  <button
                    v-for="(_, idx) in selectedProduct.images"
                    :key="idx"
                    type="button"
                    class="slider-dot"
                    :class="{ active: currentImage === idx }"
                    :aria-label="`Фото ${idx + 1}`"
                    @click.stop="currentImage = idx"
                  ></button>
                </div>
              </template>
            </div>

            <div class="modal-info">
              <div class="modal-meta">
                <span class="modal-material">{{ selectedProduct.material }}</span>
                <span class="modal-collection">Работа с мастер-класса</span>
              </div>

              <h3 class="modal-title heading-font">{{ selectedProduct.title }}</h3>

              <div class="modal-divider"></div>

              <p class="modal-desc body-font font-light">{{ selectedProduct.specs.style }}</p>

              <!-- Таб Она / Он -->
              <div class="spec-tabs" role="tablist">
                <button
                  type="button"
                  role="tab"
                  :aria-selected="activeSpecTab === 'female'"
                  :class="['spec-tab', { active: activeSpecTab === 'female' }]"
                  @click="activeSpecTab = 'female'"
                >Она</button>
                <button
                  type="button"
                  role="tab"
                  :aria-selected="activeSpecTab === 'male'"
                  :class="['spec-tab', { active: activeSpecTab === 'male' }]"
                  @click="activeSpecTab = 'male'"
                >Он</button>
              </div>

              <!-- Таблица характеристик -->
              <dl class="spec-table">
                <template v-if="activeSpecTab === 'female'">
                  <div class="spec-row">
                    <dt>Размер</dt><dd>{{ selectedProduct.specs.female.size }}</dd>
                  </div>
                  <div class="spec-row">
                    <dt>Ширина</dt><dd>{{ selectedProduct.specs.female.width }}</dd>
                  </div>
                  <div v-if="selectedProduct.specs.female.diamonds" class="spec-row">
                    <dt>Бриллианты</dt><dd>{{ selectedProduct.specs.female.diamonds }}</dd>
                  </div>
                </template>
                <template v-else>
                  <div class="spec-row">
                    <dt>Размер</dt><dd>{{ selectedProduct.specs.male.size }}</dd>
                  </div>
                  <div class="spec-row">
                    <dt>Ширина</dt><dd>{{ selectedProduct.specs.male.width }}</dd>
                  </div>
                </template>
              </dl>

              <!-- Палитра доступных металлов -->
              <div class="metals-block">
                <div class="metals-label">Доступные металлы</div>
                <div class="metals-row">
                  <span
                    v-for="m in selectedProduct.specs.metals"
                    :key="m.label"
                    class="metal-dot"
                    :style="{ background: m.color }"
                    :title="m.label"
                    :aria-label="m.label"
                  ></span>
                </div>
                <div class="metals-legend">
                  <span v-for="(m, i) in selectedProduct.specs.metals" :key="m.label">
                    {{ m.label }}<span v-if="i < selectedProduct.specs.metals.length - 1"> · </span>
                  </span>
                </div>
              </div>

              <div class="modal-divider"></div>

              <div class="modal-footer">
                <div class="modal-price-block">
                  <span class="modal-price">{{ selectedProduct.price }}</span>
                  <span class="modal-price-note">за пару · с материалами</span>
                </div>

                <a href="#contact" class="modal-cta" @click.prevent="goToBooking">
                  <span>Записаться на мастер-класс</span>
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M1 8H15M15 8L8 1M15 8L8 15" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedProduct = ref(null)
const activeSpecTab = ref('female')
const currentImage = ref(0)

// === Category filters ===
const selectedCategory = ref('Все')
const isMobileMenuOpen = ref(false)
const categories = [
  'Все',
  'Обручальные кольца',
  'Парные обручальные кольца',
  'Фактурные',
  'С бриллиантами',
  'Комбинированные',
  'Помолвочные кольца'
]

watch(selectedCategory, () => {
  visibleCount.value = VISIBLE_STEP
})

const openModal = (item) => {
  selectedProduct.value = item
  activeSpecTab.value = 'female'
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  selectedProduct.value = null
  currentImage.value = 0
  document.body.style.overflow = ''
}

const nextImage = () => {
  if (!selectedProduct.value) return
  currentImage.value = (currentImage.value + 1) % selectedProduct.value.images.length
}

const prevImage = () => {
  if (!selectedProduct.value) return
  currentImage.value = (currentImage.value - 1 + selectedProduct.value.images.length) % selectedProduct.value.images.length
}

const goToBooking = async () => {
  closeModal()
  if (router.currentRoute.value.path !== '/') {
    await router.push('/')
  }
  // Wait for modal close transition + new page mount before scrolling
  setTimeout(() => {
    const target = document.getElementById('contact')
    if (target) {
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }, 350)
}

// === "Show More" pagination ===
const VISIBLE_STEP = 8
const visibleCount = ref(VISIBLE_STEP)
const filteredItems = computed(() => {
  const visible = catalogItems.filter(item => !item.hidden)
  if (selectedCategory.value === 'Все') return visible
  return visible.filter(item => item.categories.includes(selectedCategory.value))
})
const visibleItems = computed(() => filteredItems.value.slice(0, visibleCount.value))
const hasMore = computed(() => visibleCount.value < filteredItems.value.length)
const showMore = () => {
  visibleCount.value = Math.min(visibleCount.value + VISIBLE_STEP, filteredItems.value.length)
}

// === 3D Tilt on hover ===
const MAX_TILT = 10 // degrees
const handleTilt = (e) => {
  const card = e.currentTarget
  const rect = card.getBoundingClientRect()
  const x = (e.clientX - rect.left) / rect.width
  const y = (e.clientY - rect.top) / rect.height
  const rotateX = (0.5 - y) * MAX_TILT
  const rotateY = (x - 0.5) * MAX_TILT
  card.style.setProperty('--tilt-x', `${rotateX}deg`)
  card.style.setProperty('--tilt-y', `${rotateY}deg`)
}
const resetTilt = (e) => {
  e.currentTarget.style.setProperty('--tilt-x', '0deg')
  e.currentTarget.style.setProperty('--tilt-y', '0deg')
}

const catalogItems = [
  {
    title: 'Лунные шайбы',
    desc: 'оставляем то что на сайте: "Прямые обручальные кольца «шайбы» с лунной фактурой в белом золоте."',
    price: 'от 119 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/01._Лунные_шайбы_123.webp', '/rings_new/01.2._Лунные_шайбы_123.webp', '/rings_new/01.3._Лунные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'оставляем то что на сайте: "Прямые обручальные кольца «шайбы» с лунной фактурой в белом золоте."',
      female: { size: '16', width: '3,5 мм' },
      male:   { size: '19', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайбы с Х (ИКС) прорезями',
    desc: 'Прямые обручальные кольца «шайбы» с полосками и акцентным бриллиантом в белом золоте. *Происхождение бриллиантов на выбор',
    price: 'от 136 800 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/02._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.1._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.2._Шайбы_с_Х_ИКС_прорезями_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с полосками и акцентным бриллиантом в белом золоте. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '4 мм' },
      male:   { size: '18', width: '4,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Зимний лёд',
    desc: 'Прямые шайбы с фактурой зимнего льда.',
    price: 'от 124 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/03._Зимний_лёд_123.webp', '/rings_new/03.1._Зимний_лёд_123.webp', '/rings_new/03.2._Зимний_лёд_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые шайбы с фактурой зимнего льда.',
      female: { size: '15', width: '3,5 мм' },
      male:   { size: '17', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Комбинированные шайбы',
    desc: 'Комбинированные обручальные кольца «шайбы» со вставками бриллиантов в белом и жёлтом золоте. *Происхождение бриллиантов на выбор',
    price: 'от 135 900 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/04._Комбинированные_шайбы_125.webp', '/rings_new/04.1._Комбинированные_шайбы_125.webp', '/rings_new/04.3._Комбинированные_шайбы_125.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Комбинированные'],
    specs: {
      style: 'Комбинированные обручальные кольца «шайбы» со вставками бриллиантов в белом и жёлтом золоте. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,15 ct' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Горные шайбы',
    desc: 'Прямые шайбы с фактурой «Горы».',
    price: 'от 129 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/05._Горные_шайбы_123.webp', '/rings_new/05.1._Горные_шайбы_123.webp', '/rings_new/05.2._Горные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые шайбы с фактурой «Горы».',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямые шайбы с ямчатой фактурой',
    desc: 'Полусферы с матовой ямчатой фактурой.',
    price: 'от 121 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/06._Полусферы_Ямчатые_123.webp', '/rings_new/06.1._Полусферы_Ямчатые_123.webp', '/rings_new/06.3._Полусферы_Ямчатые_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Полусферы с матовой ямчатой фактурой.',
      female: { size: '16', width: '4 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Сатиново-алмазные шайбы',
    desc: 'Прямые обручальные кольца «шайбы» с перекрёстной сатиновой и алмазной матовкой и глянцевыми краями в белом золоте',
    price: 'от 126 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/07._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.1._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.2._Сатиново-алмазные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с перекрёстной сатиновой и алмазной матовкой и глянцевыми краями в белом золоте',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайбы «Полоски»',
    desc: 'Прямые шайбы с контрастными полосками в белом золоте.',
    price: 'от 123 400 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/08._Шайбы_Полоски_123.webp', '/rings_new/08.1._Шайбы_Полоски_123.webp', '/rings_new/08.2._Шайбы_Полоски_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые шайбы с контрастными полосками в белом золоте.',
      female: { size: '16', width: '2,5 мм' },
      male:   { size: '18', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевые шайбы с прорезью',
    desc: 'Глянцевые шайбы с прорезью в белом золоте.',
    price: 'от 125 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/09._Глянцевые_шайбы_с_прорезью_123.webp', '/rings_new/09.1._Глянцевые_шайбы_с_прорезью_123.webp', '/rings_new/09.2._Глянцевые_шайбы_с_прорезью_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Глянцевые шайбы с прорезью в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайбы «Глянец и мат» с бриллиантом',
    desc: 'Прямые обручальные кольца «шайбы» с глянцевой и матовой поверхностью в белом золоте и бриллиантами 0,03 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 137 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/10._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.1._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.2._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с глянцевой и матовой поверхностью в белом золоте и бриллиантами 0,03 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Перекрут «Бесконечность»',
    desc: 'Обручальные кольца перекрут «Бесконечность» в белом золоте.',
    price: 'от 122 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/11._Перекрут_Бесконечность_12.webp', '/rings_new/11.1._Перекрут_Бесконечность_12.webp', '/rings_new/11.2._Перекрут_Бесконечность_12.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца'],
    specs: {
      style: 'Обручальные кольца перекрут «Бесконечность» в белом золоте.',
      female: { size: '16', width: '2,5 мм' },
      male:   { size: '18', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Перекрут «Бесконечность» с бриллиантами',
    desc: 'Обручальные кольца перекрут «Бесконечность» с бриллиантовой россыпью 0,25 ct. в белом золоте',
    price: 'от 138 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/12._Перекрут_Бесконечность_с_бриллиантами_124.webp', '/rings_new/12.1._Перекрут_Бесконечность_с_бриллиантами_124.webp', '/rings_new/12.2._Перекрут_Бесконечность_с_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Обручальные кольца перекрут «Бесконечность» с бриллиантовой россыпью 0,25 ct. в белом золоте',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусферы «Глянцевые ямки»',
    desc: 'Прямые обручальные кольца «шайбы» с глянцевой и матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 137 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/13._Полусферы_Глянцевые_ямки_1234.webp', '/rings_new/13.1._Полусферы_Глянцевые_ямки_1234.webp', '/rings_new/13.2._Полусферы_Глянцевые_ямки_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с глянцевой и матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '18', width: '3,5 мм' },
      male:   { size: '16', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Комфортные шайбы с бриллиантами',
    desc: 'Обручальные кольца с комфортной посадкой, матовой и глянцевой поверхностью, прорезью и вставками бриллиантов 1,5 мм в белом золоте. *Происхождение бриллиантов на выбор',
    price: 'от 135 900 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/14._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.1._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.2._Комфортные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Обручальные кольца с комфортной посадкой, матовой и глянцевой поверхностью, прорезью и вставками бриллиантов 1,5 мм в белом золоте. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,21 ct' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайбы «Грани» с бриллиантами',
    desc: 'Обручальные кольца с фактурой «Грани» и бриллиантами 1,25 мм в белом золоте.. Бриллианты 0,25 ct. *Происхождение бриллиантов на выбор',
    price: 'от 127 800 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/15._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.1._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.2._Шайбы_Грани_с_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Обручальные кольца с фактурой «Грани» и бриллиантами 1,25 мм в белом золоте.. Бриллианты 0,25 ct. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 1,25 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайбы «Волна»',
    desc: 'Прямые глянцевые шайбы с продольной фактурой «Волна» в белом золоте.',
    price: 'от 122 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/16._Шайбы_Волна_123.webp', '/rings_new/16.2._Шайбы_Волна_123.webp', '/rings_new/16.3._Шайбы_Волна_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые глянцевые шайбы с продольной фактурой «Волна» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Двухцветные шайбы с бриллиантами',
    desc: 'Составные двухцветные матовые обручальные кольца «шайбы» с глянцевыми краями и бриллиантами 1,5 мм в белом и красном золоте. *Происхождение бриллиантов на выбор.',
    price: 'от 141 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/17._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.1._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.2._Двухцветные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Составные двухцветные матовые обручальные кольца «шайбы» с глянцевыми краями и бриллиантами 1,5 мм в белом и красном золоте. *Происхождение бриллиантов на выбор.',
      female: { size: '0,19', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Двухцветные шайбы с выемками',
    desc: 'Комбинированные двухцветные обручальные кольца «шайбы» с выемками и вставками бриллиантов открытой дорожкой 2 мм. *Происхождение бриллиантов на выбор',
    price: 'от 139 950 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/18._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.1._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.2._Двухцветные_шайбы_с_выемками_1245.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'С бриллиантами', 'Комбинированные'],
    specs: {
      style: 'Комбинированные двухцветные обручальные кольца «шайбы» с выемками и вставками бриллиантов открытой дорожкой 2 мм. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,12 ct' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевые шайбы с узором и бриллиантами',
    desc: 'Прямые глянцевые шайбы. Женское — со вставкой бриллиантов огранки «Круг», мужское — гладкое глянцевое в бриллиантовой россыпью. *Происхождение бриллиантов на выбор',
    price: 'от 141 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/19._Глянцевые_шайбы_с_узором_и_бриллиантами_124.webp', '/rings_new/19.1._Глянцевые_шайбы_с_узором_и_бриллиантами_124.webp', '/rings_new/19.2._Глянцевые_шайбы_с_узором_и_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Прямые глянцевые шайбы. Женское — со вставкой бриллиантов огранки «Круг», мужское — гладкое глянцевое в бриллиантовой россыпью. *Происхождение бриллиантов на выбор',
      female: { size: '0,19', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовые полусферы «Волна»',
    desc: 'Прямые матовые шайбы с глянцевой фактурой «Волна».',
    price: 'от 125 600 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/20._Матовые_полусферы_Волна_123.webp', '/rings_new/20.1._Матовые_полусферы_Волна_123.webp', '/rings_new/20.2._Матовые_полусферы_Волна_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые матовые шайбы с глянцевой фактурой «Волна».',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Гладкие шайбы с фасками и бриллиантами',
    desc: 'Гладкие обручальные кольца «шайбы» с фасками и бриллиантами 2 мм в белом золоте. *Происхождение бриллиантов на выбор',
    price: 'от 131 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/21._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp', '/rings_new/21.1._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp', '/rings_new/21.2._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Гладкие обручальные кольца «шайбы» с фасками и бриллиантами 2 мм в белом золоте. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,2 ct' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусферы из желтого золота',
    desc: 'Гладкие обручальные кольца полусферы из желтого золота',
    price: 'от 110 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/22._Полусферы_из_желтого_золота.webp', '/rings_new/22.1._Полусферы_из_желтого_золота.webp', '/rings_new/22.2._Полусферы_из_желтого_золота.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца'],
    specs: {
      style: 'Гладкие обручальные кольца полусферы из желтого золота',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусферы из белого золота',
    desc: 'Гладкие обручальные кольца полусферы из желтого золота',
    price: 'от 110 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/23._Полусферы_из_белого_золота_12.webp', '/rings_new/23.1._Полусферы_из_белого_золота_12.webp', '/rings_new/23.2._Полусферы_из_белого_золота_12.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца'],
    specs: {
      style: 'Гладкие обручальные кольца полусферы из желтого золота',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовые полусферы',
    desc: 'Матовые обручальные кольца из белого золота',
    price: 'от 110 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/24._Матовые_полусферы_123.webp', '/rings_new/24.1._Матовые_полусферы_123.webp', '/rings_new/24.2._Матовые_полусферы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Матовые обручальные кольца из белого золота',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Кольцо с фактурой "Барханы"',
    desc: 'Кольцо из белого золота с фактурой "Барханы"',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/25._Кольцо_с_фактурой_Барханы_13.webp', '/rings_new/25.1._Кольцо_с_фактурой_Барханы_13.webp', '/rings_new/25.2._Кольцо_с_фактурой_Барханы_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Кольцо из белого золота с фактурой "Барханы"',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Кольцо с бриллиантовой дорожкой',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,2 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 70 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/26._Кольцо_с_бриллиантовой_дорожкой_14.webp', '/rings_new/26.1._Кольцо_с_бриллиантовой_дорожкой_14.webp', '/rings_new/26.2._Кольцо_с_бриллиантовой_дорожкой_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,2 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Кольцо с россыпью бриллиантов и выемкой',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,25 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 73 000 ₽ .',
    material: 'Металл на выбор',
    images: ['/rings_new/27._Кольцо_с_россыпью_бриллиантов_и_выемкой_14.webp', '/rings_new/27.1._Кольцо_с_россыпью_бриллиантов_и_выемкой_14.webp', '/rings_new/27.2._Кольцо_с_россыпью_бриллиантов_и_выемкой_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,25 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '2,2 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусфера поперечное "Дерево"',
    desc: 'Полусфера из белого золото с поперечной фактурой "Дерево"',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/28._Полусфера_поперечное_Дерево_13.webp', '/rings_new/28.1._Полусфера_поперечное_Дерево_13.webp', '/rings_new/28.2._Полусфера_поперечное_Дерево_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Полусфера из белого золото с поперечной фактурой "Дерево"',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Кольцо "Половинка"',
    desc: 'Кольцо из белого золота с глянцевой и продольной матовой фактурой в полоину кольца',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/29._Кольцо_Половинка_135.webp', '/rings_new/29.1._Кольцо_Половинка_135.webp', '/rings_new/29.2._Кольцо_Половинка_135.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'Комбинированные'],
    specs: {
      style: 'Кольцо из белого золота с глянцевой и продольной матовой фактурой в полоину кольца',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайба поперечное "Дерево"',
    desc: 'Шайба из белого золота с поперечной фактурой "Дерево"',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/30._Шайба_поперечное_Дерево_13.webp', '/rings_new/30.1._Шайба_поперечное_Дерево_13.webp', '/rings_new/30.2._Шайба_поперечное_Дерево_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Шайба из белого золота с поперечной фактурой "Дерево"',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайба с фактурой "Волна"',
    desc: 'Шайба из белого золота с поперечной фактурой "Волна"',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/31._Шайба_с_фактурой_Волна_13.webp', '/rings_new/31.1._Шайба_с_фактурой_Волна_13.webp', '/rings_new/31.2._Шайба_с_фактурой_Волна_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Шайба из белого золота с поперечной фактурой "Волна"',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Бриллиантовая дорожка в 1/3 кольца',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,17 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 71 000 ₽ .',
    material: 'Металл на выбор',
    images: ['/rings_new/32._Бриллиантовая_дорожка_в_13_кольца_14.webp', '/rings_new/32.1._Бриллиантовая_дорожка_в_13_кольца_14.webp', '/rings_new/32.3._Бриллиантовая_дорожка_в_13_кольца_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,17 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '2 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Россыпь бриллиантов в 1/4 кольца',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,2 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 73 000 ₽ .',
    material: 'Металл на выбор',
    images: ['/rings_new/33._Россыпь_бриллиантов_в_14_кольца_14.webp', '/rings_new/33.1._Россыпь_бриллиантов_в_1.4_кольца_14.webp', '/rings_new/33.3._Россыпь_бриллиантов_в_1.4_кольца_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,2 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Дорожка закрытая в 1/2 кольца',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,22 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 75 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/34._Дорожка_закрытая_в_12_кольца_14.webp', '/rings_new/34.1._Дорожка_закрытая_в_12_кольца_14.webp', '/rings_new/34.3._Дорожка_закрытая_в_12_кольца_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,22 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '2,2 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Открытая дорожка из бриллиантов изумрудного цвета',
    desc: 'Кольцо из белого золота с дорожкой из бриллиантов изумрудного цвета 0,22 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 73 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/35._Открытая_дорожка_из_бриллиантов_изумрудного_цвета.webp', '/rings_new/35.1._Открытая_дорожка_из_бриллиантов_изумрудного_цвета.webp', '/rings_new/35.3._Открытая_дорожка_из_бриллиантов_изумрудного_цвета.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с дорожкой из бриллиантов изумрудного цвета 0,22 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '2 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Открытая россыпь бриллиантов в 1/4 кольца',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью цвета 0,22 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 75 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/36._Открытая_россыпь_бриллиантов_в_1.4_кольца_14.webp', '/rings_new/36.1._Открытая_россыпь_бриллиантов_в_1.4_кольца_14.webp', '/rings_new/36.2._Открытая_россыпь_бриллиантов_в_1.4_кольца_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью цвета 0,22 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Отпечаток пальчика внутри кольца',
    desc: 'Кольцо любой формы из белого золота с отпечатком пальца с внутренней или внешней стороны колечка',
    price: 'от 55 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/37._Отпечаток_пальчика_внутри_кольца_13.webp', '/rings_new/37.1._Отпечаток_пальчика_внетри_кольца_13.webp', '/rings_new/37.2._Отпечаток_пальчика_внутри_кольца_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Кольцо любой формы из белого золота с отпечатком пальца с внутренней или внешней стороны колечка',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16,5', width: '4,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Бриллиантовая россыпь в половину колечка',
    desc: 'Кольцо из белого золота с бриллиантовой россыпью 0,22 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 73 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/38._Бриллиантовая_россыпь_в_половину_колечка_14.webp', '/rings_new/38.1._Бриллиантовая_россыпь_в_половину_колечка_14.webp', '/rings_new/38.2._Бриллиантовая_россыпь_в_половину_колечка_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой россыпью 0,22 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '1,7 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовое кольцо с волной',
    desc: 'Шайба из белого золота с продольной волной',
    price: 'от 50 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/39._Матовое_кольцо_с_волной_13.webp', '/rings_new/39.1._Матовое_кольцо_с_волной_13.webp', '/rings_new/39.2._Матовое_кольцо_с_волной_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Шайба из белого золота с продольной волной',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с бриллиантами 3х3',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,2 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 77 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/40._Глянцевая_шайба_с_бриллиантами_3х3_14.webp', '/rings_new/40.1._Глянцевая_шайба_с_бриллиантами_3х3_14.webp', '/rings_new/40.2._Глянцевая_шайба_с_бриллиантами_3х3_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,2 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусфера с роскошной россыпью камней',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,27 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 79 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/41._Полусфера_с_роскошной_россыпью_камней_14.webp', '/rings_new/41.1._Полусфера_с_роскошной_россыпью_камней_14.webp', '/rings_new/41.2._Полусфера_с_роскошной_россыпью_камней_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,27 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '15', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: '42. Шайба с хаотичной матовкой',
    desc: 'Прямая шайба из белого золота с хаотичной матовкой по всей окружности',
    price: 'от 51 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/42._Шайба_с_хаотичной_матовкой_13.webp', '/rings_new/42.1._Шайба_с_хаотичной_матовкой_13.webp', '/rings_new/42.2._Шайба_с_хаотичной_матовкой_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямая шайба из белого золота с хаотичной матовкой по всей окружности',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая матовая шайба с ямчатой фактурой',
    desc: 'Обручальное кольцо шайба с матовой ямчатой фактурой в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/06._Полусферы_Ямчатые_123.webp', '/rings_new/06.1._Полусферы_Ямчатые_123.webp', '/rings_new/06.3._Полусферы_Ямчатые_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Обручальное кольцо шайба с матовой ямчатой фактурой в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с фасками и бриллиантами',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,15 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 78 500₽',
    material: 'Металл на выбор',
    images: ['/rings_new/21._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp', '/rings_new/21.1._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp', '/rings_new/21.2._Гладкие_шайбы_с_фасками_и_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,15 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '15', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая глянцевая шайба с узором и бриллиантми',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,12 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 72 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/14._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.1._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.2._Комфортные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,12 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '15', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая глянцевая шайба с узором и бриллиантми',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,1 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 73 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/14._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.1._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.2._Комфортные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,1 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Комбинированная матовая и глянцевая шайба со вставками бриллиантов',
    desc: 'Комбинированное кольцо из красного и белого золота с бриллиантовой вставкой 0,03 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 80 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/17._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.1._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.2._Двухцветные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами', 'Комбинированные'],
    specs: {
      style: 'Комбинированное кольцо из красного и белого золота с бриллиантовой вставкой 0,03 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Комбинированная матовая и глянцевая шайба со вставками черных бриллиантов',
    desc: 'Комбинированное кольцо из красного и белого золота с бриллиантовой вставкой 0,05 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 80 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/17._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.1._Двухцветные_шайбы_с_бриллиантами_1234.webp', '/rings_new/17.2._Двухцветные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами', 'Комбинированные'],
    specs: {
      style: 'Комбинированное кольцо из красного и белого золота с бриллиантовой вставкой 0,05 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая матовая шайба с фасками и узором',
    desc: 'Матовая шайба с прорезями из белого золота',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/14._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.1._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.2._Комфортные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Матовая шайба с прорезями из белого золота',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая глянцевая шайба с узором и бриллиантми',
    desc: 'Кольцо из белого золота с бриллиантовой вставкой 0,12 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 75 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/14._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.1._Комфортные_шайбы_с_бриллиантами_1234.webp', '/rings_new/14.2._Комфортные_шайбы_с_бриллиантами_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Кольцо из белого золота с бриллиантовой вставкой 0,12 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба с сатиновой матовкой',
    desc: 'Прямая «шайбы» с перекрёстной сатиновой матовкой и глянцевыми краями в белом золоте',
    price: 'от 58 900 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/07._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.1._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.2._Сатиново-алмазные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямая «шайбы» с перекрёстной сатиновой матовкой и глянцевыми краями в белом золоте',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с фасками',
    desc: 'Прямая «шайбы» с алмазной матовкой и глянцевыми краями в белом золоте',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/07._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.1._Сатиново-алмазные_шайбы_123.webp', '/rings_new/07.2._Сатиново-алмазные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямая «шайбы» с алмазной матовкой и глянцевыми краями в белом золоте',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба "Зимний лёд"',
    desc: 'Прямые обручальные кольца «шайбы» с фактурой «Зимний лёд» в белом золоте.',
    price: 'от 62 500 ₽ .',
    material: 'Металл на выбор',
    images: ['/rings_new/03._Зимний_лёд_123.webp', '/rings_new/03.1._Зимний_лёд_123.webp', '/rings_new/03.2._Зимний_лёд_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с фактурой «Зимний лёд» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусфера матовая с фактурой "Грани"',
    desc: 'Обручальное кольца полусфера с матовой ямчатой фактурой в белом золоте.',
    price: 'от 60 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/20._Матовые_полусферы_Волна_123.webp', '/rings_new/20.1._Матовые_полусферы_Волна_123.webp', '/rings_new/20.2._Матовые_полусферы_Волна_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Обручальное кольца полусфера с матовой ямчатой фактурой в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба с лунной фактурой',
    desc: 'Прямая «шайба» с лунной фактурой в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/01._Лунные_шайбы_123.webp', '/rings_new/01.2._Лунные_шайбы_123.webp', '/rings_new/01.3._Лунные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямая «шайба» с лунной фактурой в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '19', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с романтичной пропилом',
    desc: 'Глянцевое обручальное кольцо с прорезью в белом золоте',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/09._Глянцевые_шайбы_с_прорезью_123.webp', '/rings_new/09.1._Глянцевые_шайбы_с_прорезью_123.webp', '/rings_new/09.2._Глянцевые_шайбы_с_прорезью_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Глянцевое обручальное кольцо с прорезью в белом золоте',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба с "Икс" узорами',
    desc: 'Прямое обручальное кольцо с полосками в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/02._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.1._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.2._Шайбы_с_Х_ИКС_прорезями_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямое обручальное кольцо с полосками в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '17', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба с фаткурой "Лёд"',
    desc: 'Прямые обручальные кольца «шайбы» с фактурой «Зимний лёд» в белом золоте.',
    price: 'от 62 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/03._Зимний_лёд_123.webp', '/rings_new/03.1._Зимний_лёд_123.webp', '/rings_new/03.2._Зимний_лёд_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с фактурой «Зимний лёд» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '17', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба с "Икс" узорами',
    desc: 'Прямая шайба из белого золота с ИКС-узоррами',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/02._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.1._Шайбы_с_Х_ИКС_прорезями_123.webp', '/rings_new/02.2._Шайбы_с_Х_ИКС_прорезями_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямая шайба из белого золота с ИКС-узоррами',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '4,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая глянцевая шайба с бриллиантовой дорожкой в край',
    desc: 'Комбинированное обручальное кольцо со вставками бриллиантов 0,15 ct. жёлтом золоте. *Происхождение бриллиантов на выбор',
    price: 'от 79 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/04._Комбинированные_шайбы_125.webp', '/rings_new/04.1._Комбинированные_шайбы_125.webp', '/rings_new/04.3._Комбинированные_шайбы_125.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами', 'Комбинированные'],
    specs: {
      style: 'Комбинированное обручальное кольцо со вставками бриллиантов 0,15 ct. жёлтом золоте. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Комбинированная глянцевая шайба с золотой вставкой',
    desc: 'Комбинированное обручальное кольцо со вставкой жёлтого золота.',
    price: 'от 72 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/04._Комбинированные_шайбы_125.webp', '/rings_new/04.1._Комбинированные_шайбы_125.webp', '/rings_new/04.3._Комбинированные_шайбы_125.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Комбинированные'],
    specs: {
      style: 'Комбинированное обручальное кольцо со вставкой жёлтого золота.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба "Фантазия"',
    desc: 'Комбинированное кольцо из белого золота',
    price: 'от 75 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/18._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.1._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.2._Двухцветные_шайбы_с_выемками_1245.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Комбинированные'],
    specs: {
      style: 'Комбинированное кольцо из белого золота',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Прямая шайба "Фантазия" с бриллиантовой россыпью',
    desc: 'Комбинированное двухцветное кольцо с выемками и вставками бриллиантов открытой дорожкой 2 мм.',
    price: 'от 89 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/18._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.1._Двухцветные_шайбы_с_выемками_1245.webp', '/rings_new/18.2._Двухцветные_шайбы_с_выемками_1245.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами', 'Комбинированные'],
    specs: {
      style: 'Комбинированное двухцветное кольцо с выемками и вставками бриллиантов открытой дорожкой 2 мм.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба "Грани"',
    desc: 'Обручальное кольцо с фактурой «Грани» в белом золоте.',
    price: 'от 59 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/15._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.1._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.2._Шайбы_Грани_с_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Обручальное кольцо с фактурой «Грани» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с фактурой "Грани" и бриллиантами',
    desc: 'Обручальное кольцо с фактурой «Грани» и бриллиантами 1,25 мм в белом золоте.. Бриллианты 0,25 ct. *Происхождение бриллиантов на выбор',
    price: 'от 68 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/15._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.1._Шайбы_Грани_с_бриллиантами_124.webp', '/rings_new/15.2._Шайбы_Грани_с_бриллиантами_124.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Обручальное кольцо с фактурой «Грани» и бриллиантами 1,25 мм в белом золоте.. Бриллианты 0,25 ct. *Происхождение бриллиантов на выбор',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм', diamonds: 'Круг · 0,25 ct' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба "Горы"',
    desc: 'Обручальные кольцо «шайба» с фактурой «Горы» в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/05._Горные_шайбы_123.webp', '/rings_new/05.1._Горные_шайбы_123.webp', '/rings_new/05.2._Горные_шайбы_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Обручальные кольцо «шайба» с фактурой «Горы» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Лунная глянцевая шайба с бриллиантом',
    desc: 'Прямое обручальное кольцо «шайбы» с глянцевой лунной фактурой в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 69 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/13._Полусферы_Глянцевые_ямки_1234.webp', '/rings_new/13.1._Полусферы_Глянцевые_ямки_1234.webp', '/rings_new/13.2._Полусферы_Глянцевые_ямки_1234.webp'],
    bestseller: false,
    categories: ['Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Прямое обручальное кольцо «шайбы» с глянцевой лунной фактурой в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с фактурой "Волна"',
    desc: 'Прямое глянцевое обручальное кольцо с продольной фактурой «Волна» в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/16._Шайбы_Волна_123.webp', '/rings_new/16.2._Шайбы_Волна_123.webp', '/rings_new/16.3._Шайбы_Волна_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямое глянцевое обручальное кольцо с продольной фактурой «Волна» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовая шайба с фактурой "Волна"',
    desc: 'Прямое матовое обручальное кольцо с продольной фактурой «Волна» в белом золоте.',
    price: 'от 62 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/16._Шайбы_Волна_123.webp', '/rings_new/16.2._Шайбы_Волна_123.webp', '/rings_new/16.3._Шайбы_Волна_123.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Прямое матовое обручальное кольцо с продольной фактурой «Волна» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовая прямая шайба с бриллиантовой вставкой',
    desc: 'Прямое обручальное кольцо «шайба» с матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 68 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/10._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.1._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.2._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Прямое обручальное кольцо «шайба» с матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '18', width: '5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая прямая шайба с бриллиантовой вставкой',
    desc: 'Прямое обручальное кольцо «шайба» с матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
    price: 'от 68 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/10._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.1._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp', '/rings_new/10.2._Шайбы_Глянец_и_мат_с_бриллиантом_1234.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'С бриллиантами'],
    specs: {
      style: 'Прямое обручальное кольцо «шайба» с матовой поверхностью в белом золоте и бриллиантом 0,012 ct. *Происхождение бриллиантов на выбор.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '3 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянвая шаба "Бесконечность"',
    desc: 'Обручальные кольца перекрут «Бесконечность» в белом золоте.',
    price: 'от 59 500 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/11._Перекрут_Бесконечность_12.webp', '/rings_new/11.1._Перекрут_Бесконечность_12.webp', '/rings_new/11.2._Перекрут_Бесконечность_12.webp'],
    bestseller: false,
    categories: ['Обручальные кольца'],
    specs: {
      style: 'Обручальные кольца перекрут «Бесконечность» в белом золоте.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '2,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Глянцевая шайба с россыпью бриллиантов',
    desc: 'Обручальное кольцо из желтого золото шириной АЖ 10 мм и бриллиантовой дорожкой в 0,3 ct.',
    price: 'от 187 500₽',
    material: 'Металл на выбор',
    images: ['/rings_new/43._Глянцевая_шайба_с_россыпью_бриллиантов_14.webp', '/rings_new/43.1._Глянцевая_шайба_с_россыпью_бриллиантов_14.webp', '/rings_new/43.2._Глянцевая_шайба_с_россыпью_бриллиантов_14.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'С бриллиантами'],
    specs: {
      style: 'Обручальное кольцо из желтого золото шириной АЖ 10 мм и бриллиантовой дорожкой в 0,3 ct.',
      female: { size: '16', width: '3 мм' },
      male:   { size: '16', width: '10 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Изгибы глянцевые',
    desc: 'Роскошные обручальные кольца «Изгибы» из белого и жёлтого золота. Созданы по 3D-модели.',
    price: 'от 120 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/44._Изгибы_1235.webp', '/rings_new/44.4._Изгибы_глянцевые_1235.webp', '/rings_new/44.1._Изгибы_глянцевые_1235.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Парные обручальные кольца', 'Фактурные', 'Комбинированные'],
    specs: {
      style: 'Роскошные обручальные кольца «Изгибы» из белого и жёлтого золота. Созданы по 3D-модели.',
      female: { size: '15', width: '2,5 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Изгибы глянцевые белые',
    desc: 'Глянцевое обручальное кольцо с изгибами из белого золота. Создано по 3D-модели.',
    price: 'от 60 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/44.6._Изгибы_глянцевые_1235.webp', '/rings_new/44.4._Изгибы_глянцевые_1235.webp', '/rings_new/44.5._Изгибы_глянцевые_1235.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Глянцевое обручальное кольцо с изгибами из белого золота. Создано по 3D-модели.',
      female: { size: '15', width: '2,5 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Изгибы глянцевые жёлтые',
    desc: 'Глянцевое обручальное кольцо с изгибами из жёлтого золота. Создано по 3D-модели.',
    price: 'от 60 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/44.2._Изгибы_глянцевые_1235.webp', '/rings_new/44.1._Изгибы_глянцевые_1235.webp', '/rings_new/44.3._Изгибы_глянцевые_1235.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Глянцевое обручальное кольцо с изгибами из жёлтого золота. Создано по 3D-модели.',
      female: { size: '15', width: '2,5 мм' },
      male:   { size: '18', width: '3,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайба «Перламутр»',
    desc: 'Яркое обручальное кольцо из белого золота с перламутровой фактурой.',
    price: 'от 60 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/45._Шайба_Перламутр_13.webp', '/rings_new/45.2._Шайба_Перламутр_13.webp', '/rings_new/45.3._Шайба_Перламутр_13.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные'],
    specs: {
      style: 'Яркое обручальное кольцо из белого золота с перламутровой фактурой.',
      female: { size: '17', width: '3,5 мм' },
      male:   { size: '18', width: '4 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Шайба «Перламутр» с чёрной эмалью',
    desc: 'Потрясающее обручальное кольцо из белого золота со вставкой чёрной эмали. Цвет эмали можно выбрать любой.',
    price: 'от 70 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/46._Шайба_Перламутр_со_вставкой_черной_эмали_135.webp', '/rings_new/46.1._Шайба_Перламутр_со_вставкой_черной_эмали_135.webp', '/rings_new/46.3._Шайба_Перламутр_со_вставкой_черной_эмали_135.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'Комбинированные'],
    specs: {
      style: 'Потрясающее обручальное кольцо из белого золота со вставкой чёрной эмали. Цвет эмали можно выбрать любой.',
      female: { size: '18', width: '5 мм' },
      male:   { size: '19', width: '5,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Полусферы «Тринити»',
    desc: 'Глянцевые полусферы «Тринити» из белого, жёлтого и красного золота. Можно изготовить с любой фактурой на выбор.',
    price: 'от 85 000 ₽',
    material: 'Металл на выбор',
    images: ['/rings_new/47._Полусферы_Тринити_135.webp', '/rings_new/47.1._Полусферы_Тринити_135.webp', '/rings_new/47.3._Полусферы_Тринити_135.webp'],
    bestseller: false,
    categories: ['Обручальные кольца', 'Фактурные', 'Комбинированные'],
    specs: {
      style: 'Глянцевые полусферы «Тринити» из белого, жёлтого и красного золота. Можно изготовить с любой фактурой на выбор.',
      female: { size: '16', width: '2 мм' },
      male:   { size: '17', width: '2,5 мм' },
      metals: [
        { label: 'Серебро 925',            color: '#C7C9CE' },
        { label: 'Белое золото 585/750',   color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750',  color: '#E5C56A' },
        { label: 'Красное золото 585/750', color: '#C8775A' },
        { label: 'Розовое золото 585/750', color: '#E5B6A6' },
        { label: 'Платина 950',            color: '#D6D8DC' }
      ]
    }
  },
]
</script>

<style scoped>
/* ===========================================
   Premium Catalog Card — minimal luxury
   =========================================== */

.catalog-card {
  --tilt-x: 0deg;
  --tilt-y: 0deg;
  perspective: 1200px;
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 0 !important;
  position: relative;
}

.catalog-card-inner {
  display: flex;
  flex-direction: column;
  transform: rotateX(var(--tilt-x)) rotateY(var(--tilt-y));
  -webkit-transform: rotateX(var(--tilt-x)) rotateY(var(--tilt-y));
  transform-style: preserve-3d;
  -webkit-transform-style: preserve-3d;
  transition: transform 0.15s ease-out;
  -webkit-transition: -webkit-transform 0.15s ease-out;
  will-change: transform;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

.catalog-card:not(:hover) .catalog-card-inner {
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  -webkit-transition: -webkit-transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Disable 3D tilt on touch devices to avoid iOS Safari rendering bugs */
@media (hover: none) and (pointer: coarse) {
  .catalog-card {
    perspective: none;
  }

  .catalog-card-inner,
  .catalog-card:hover .catalog-card-inner,
  .catalog-card:not(:hover) .catalog-card-inner {
    transform: none !important;
    -webkit-transform: none !important;
    transform-style: flat;
    -webkit-transform-style: flat;
    will-change: auto;
  }
}

/* === Image area === */
.catalog-card :deep(.catalog-img) {
  width: 100%;
  aspect-ratio: 4/5;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1.5rem;
  background: rgba(255, 255, 255, 0.02);
  position: relative;
  transform: translateZ(0);
  box-shadow:
    0 1px 0 0 rgba(255, 255, 255, 0.04) inset,
    0 8px 24px -12px rgba(0, 0, 0, 0.5);
  transition: box-shadow 0.5s ease;
  flex-shrink: 0;
}

.catalog-card:hover :deep(.catalog-img) {
  box-shadow:
    0 1px 0 0 rgba(222, 186, 78, 0.15) inset,
    0 18px 40px -10px rgba(0, 0, 0, 0.7),
    0 0 0 1px rgba(222, 186, 78, 0.15);
}

.catalog-card :deep(.catalog-img img) {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  -webkit-object-fit: cover;
  transition: transform 0.8s cubic-bezier(0.22, 1, 0.36, 1);
}

.catalog-card:hover :deep(.catalog-img img) {
  transform: scale(1.06);
}

/* === Bestseller badge — gold outline === */
.catalog-card :deep(.bestseller-badge) {
  position: absolute;
  top: 1rem;
  left: 1rem;
  bottom: auto;
  background: rgba(8, 6, 4, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(222, 186, 78, 0.4);
  color: var(--color-gold-light);
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  font-size: 0.65rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-weight: 400;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 2;
  transition: opacity 0.4s ease, visibility 0.4s ease;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-gold);
  box-shadow: 0 0 8px var(--color-gold);
  animation: dotPulse 2s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Hide bestseller on hover (overlay covers it) */
.catalog-card:hover :deep(.bestseller-badge) {
  opacity: 0;
  visibility: hidden;
}

/* === Overlay === */
.catalog-card :deep(.overlay) {
  background: linear-gradient(to top, rgba(8, 6, 4, 0.9) 0%, rgba(8, 6, 4, 0.3) 50%, transparent 100%);
  z-index: 3;
}

.catalog-card :deep(.overlay-btn) {
  border: 1px solid rgba(222, 186, 78, 0.5);
  color: var(--color-gold-light);
  background: rgba(8, 6, 4, 0.4);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  padding: 0.85rem 1.5rem;
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  font-weight: 400;
  pointer-events: auto;
  position: relative;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.85rem;
  width: 100%;
  transition: all 0.35s ease;
}

.catalog-card :deep(.overlay-btn:hover) {
  background: var(--color-gold);
  border-color: var(--color-gold);
  color: #0a0a0a;
}

.overlay-btn-arrow {
  transition: transform 0.35s ease;
}

.catalog-card :deep(.overlay-btn:hover) .overlay-btn-arrow {
  transform: translate(2px, -2px);
}

/* === Info section below image === */
.catalog-info {
  display: flex;
  flex-direction: column;
  padding: 0 0.25rem;
  flex-shrink: 0;
  min-width: 0;
}

.catalog-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.85rem;
}

.catalog-index {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  color: var(--color-text-muted);
  opacity: 0.5;
}

.catalog-material {
  font-family: var(--font-body);
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-gold);
  text-align: right;
  flex: 1;
}

.catalog-card :deep(.product-title) {
  font-size: 1.4rem;
  letter-spacing: 0.01em;
  margin-bottom: 0.5rem;
  font-weight: 400;
  color: var(--color-text);
  transition: color 0.3s ease;
}

.catalog-card:hover :deep(.product-title) {
  color: var(--color-gold-light);
}

.catalog-card :deep(.product-desc) {
  font-size: 0.85rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  opacity: 0.75;
  margin-bottom: 1.25rem;
  min-height: 2.7rem;
}

.catalog-divider {
  height: 1px;
  background: linear-gradient(to right, rgba(222, 186, 78, 0.3), transparent);
  margin-bottom: 1rem;
}

.catalog-card :deep(.product-price) {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 400;
  letter-spacing: 0.02em;
  color: var(--color-gold-light);
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
}

.price-from {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  opacity: 0.6;
  font-weight: 300;
}

/* === Hover effect on whole card === */
.catalog-card {
  transition: transform 0.5s cubic-bezier(0.22, 1, 0.36, 1) !important;
}

.catalog-card:hover {
  transform: translateY(-6px) !important;
}

.catalog-card.bestseller {
  transform: translateY(-12px) !important;
}

.catalog-card.bestseller:hover {
  transform: translateY(-18px) !important;
}

@media (max-width: 1024px) {
  .catalog-card.bestseller,
  .catalog-card.bestseller:hover {
    transform: translateY(0) !important;
  }
  .catalog-card:hover {
    transform: translateY(-4px) !important;
  }

  /* Minimal card view on tablets and mobile: photo + title + price only */
  .catalog-card :deep(.catalog-img) {
    margin-bottom: 0.75rem;
  }

  .catalog-card :deep(.product-desc),
  .catalog-meta,
  .catalog-divider {
    display: none;
  }
}

@media (max-width: 640px) {
  .catalog-card :deep(.catalog-img) {
    margin-bottom: 0.5rem;
  }

  .catalog-card :deep(.product-title) {
    font-size: 0.9rem;
    letter-spacing: 0;
  }

  .catalog-card :deep(.product-desc) {
    font-size: 0.75rem;
    margin-bottom: 0.85rem;
    min-height: auto;
  }

  .catalog-card :deep(.product-price) {
    font-size: 0.85rem;
    white-space: nowrap;
  }

  .catalog-meta {
    margin-bottom: 0.6rem;
  }

  .catalog-index,
  .catalog-material {
    font-size: 0.6rem;
  }

  .catalog-divider {
    margin-bottom: 0.75rem;
  }
}

@media (max-width: 400px) {
  .catalog-card :deep(.product-title) {
    font-size: 0.8rem;
  }

  .catalog-card :deep(.product-price) {
    font-size: 0.8rem;
  }
}

/* === Show More button === */
.catalog-title {
  margin-top: 2.25rem;
}

.catalog-title-gold {
  color: var(--color-gold);
}

.catalog-lead {
  max-width: 620px;
  margin: 1.5rem auto 0;
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--color-text-muted);
  font-style: italic;
}

@media (max-width: 768px) {
  .catalog-lead {
    font-size: 0.875rem;
    padding: 0 1rem;
  }
}

/* === Category filters === */
.category-filter {
  position: relative;
  z-index: 50;
  margin: 2rem 0 2.5rem;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.6rem;
}

.category-btn {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(222, 186, 78, 0.22);
  border-radius: 999px;
  padding: 0.55rem 1rem;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.category-btn:hover {
  color: var(--color-gold-light);
  border-color: rgba(222, 186, 78, 0.55);
  background: rgba(222, 186, 78, 0.08);
}

.category-btn.active {
  color: var(--color-gold-light);
  background: rgba(222, 186, 78, 0.14);
  border-color: rgba(222, 186, 78, 0.65);
}

/* Mobile category menu */
.category-mobile {
  display: none;
  position: relative;
  width: 100%;
}

.category-burger {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  width: 100%;
  padding: 0.8rem 1rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(222, 186, 78, 0.22);
  border-radius: 8px;
  cursor: pointer;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.burger-line {
  width: 18px;
  height: 1.5px;
  background: var(--color-gold-light);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.burger-label {
  font-family: var(--font-body);
  font-size: 0.75rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text);
}

.category-mobile-menu {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  padding: 0.6rem;
  background: rgba(12, 10, 8, 0.78);
  border: 1px solid rgba(222, 186, 78, 0.28);
  border-radius: 10px;
  backdrop-filter: blur(22px) saturate(140%);
  -webkit-backdrop-filter: blur(22px) saturate(140%);
  box-shadow:
    0 1px 0 0 rgba(255, 255, 255, 0.04) inset,
    0 20px 50px -15px rgba(0, 0, 0, 0.8);
}

.category-mobile-item {
  font-family: var(--font-body);
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-align: left;
  color: var(--color-text-muted);
  background: transparent;
  border: none;
  border-radius: 6px;
  padding: 0.7rem 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-mobile-item:hover,
.category-mobile-item.active {
  color: var(--color-gold-light);
  background: rgba(222, 186, 78, 0.12);
}

/* Category menu transition */
.category-menu-enter-active,
.category-menu-leave-active {
  transition: all 0.25s ease;
}

.category-menu-enter-from,
.category-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 900px) {
  .category-list {
    display: none;
  }

  .category-mobile {
    display: block;
    padding: 0 0.5rem;
  }
}

.show-more-wrap {
  display: flex;
  justify-content: center;
  margin-top: 3.5rem;
}

.show-more-btn {
  background: transparent;
  border: 1px solid rgba(212, 165, 116, 0.4);
  color: var(--color-text);
  padding: 1rem 2.5rem;
  border-radius: 9999px;
  font-family: var(--font-body);
  font-size: 0.85rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  font-weight: 400;
  cursor: pointer;
  transition: all 0.4s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
  position: relative;
  overflow: hidden;
}

.show-more-btn::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at center, rgba(222, 186, 78, 0.15), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.show-more-btn:hover {
  border-color: var(--color-gold);
  color: var(--color-gold);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px -8px rgba(222, 186, 78, 0.3);
}

.show-more-btn:hover::before {
  opacity: 1;
}

.show-more-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 28px;
  height: 24px;
  padding: 0 0.5rem;
  border-radius: 999px;
  background: rgba(222, 186, 78, 0.15);
  color: var(--color-gold);
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  font-weight: 500;
  position: relative;
  z-index: 1;
}

/* ===========================================
   Premium Product Modal
   =========================================== */

/* Overlay transitions */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.4s ease, backdrop-filter 0.4s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-content-enter-active {
  transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}
.modal-content-leave-active {
  transition: all 0.3s ease;
}
.modal-content-enter-from {
  opacity: 0;
  transform: translateY(20px) scale(0.96);
}
.modal-content-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.98);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(3, 8, 6, 0.88);
  backdrop-filter: blur(16px) saturate(140%);
  -webkit-backdrop-filter: blur(16px) saturate(140%);
  z-index: 100;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

/* Subtle gold + emerald radial glows behind modal */
.modal-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 30% 30%, rgba(222, 186, 78, 0.07), transparent 55%),
    radial-gradient(ellipse at 70% 75%, rgba(16, 185, 129, 0.08), transparent 50%);
  pointer-events: none;
}

.modal-content {
  background:
    radial-gradient(ellipse at 90% 100%, rgba(6, 78, 59, 0.18), transparent 50%),
    linear-gradient(160deg, rgba(20, 26, 22, 0.96), rgba(8, 12, 10, 0.98));
  border: 1px solid rgba(222, 186, 78, 0.18);
  border-radius: 6px;
  padding: 3.5rem;
  max-width: 1000px;
  width: 100%;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 3.5rem;
  position: relative;
  box-shadow:
    0 50px 100px -20px rgba(0, 0, 0, 0.8),
    0 0 80px -20px rgba(16, 185, 129, 0.1),
    0 0 0 1px rgba(222, 186, 78, 0.05) inset,
    0 1px 0 0 rgba(255, 255, 255, 0.04) inset;
  max-height: 90vh;
  overflow-y: auto;
}

/* Hide scrollbar */
.modal-content::-webkit-scrollbar { width: 0; }
.modal-content { scrollbar-width: none; }

/* Decorative corner accents — gold top-left, emerald bottom-right */
.modal-content::before,
.modal-content::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 24px;
  pointer-events: none;
}
.modal-content::before {
  top: 12px;
  left: 12px;
  border-top: 1px solid rgba(222, 186, 78, 0.5);
  border-left: 1px solid rgba(222, 186, 78, 0.5);
}
.modal-content::after {
  bottom: 12px;
  right: 12px;
  border-bottom: 1px solid rgba(52, 211, 153, 0.45);
  border-right: 1px solid rgba(52, 211, 153, 0.45);
}

/* Close button */
.modal-close {
  position: absolute;
  top: 1.25rem;
  right: 1.25rem;
  background: transparent;
  border: 1px solid rgba(222, 186, 78, 0.3);
  color: rgba(232, 201, 160, 0.7);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}
.modal-close:hover {
  background: rgba(222, 186, 78, 0.1);
  border-color: var(--color-gold);
  color: var(--color-gold-light);
  transform: rotate(90deg);
}

/* Image side */
.modal-image-wrapper {
  position: relative;
  border-radius: 4px;
  overflow: hidden;
  aspect-ratio: 4/5;
  box-shadow:
    0 1px 0 0 rgba(255, 255, 255, 0.04) inset,
    0 0 0 1px rgba(222, 186, 78, 0.1),
    0 20px 50px -15px rgba(0, 0, 0, 0.8);
}

.modal-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.modal-bestseller {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(8, 6, 4, 0.7);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(222, 186, 78, 0.4);
  color: var(--color-gold-light);
  padding: 0.4rem 0.85rem;
  border-radius: 999px;
  font-size: 0.65rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  z-index: 5;
}

/* Image slider controls */
.slider-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  border: 1px solid rgba(222, 186, 78, 0.35);
  background: rgba(8, 6, 4, 0.55);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: var(--color-gold-light);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
  z-index: 6;
}

.slider-arrow:hover {
  background: rgba(222, 186, 78, 0.18);
  border-color: rgba(222, 186, 78, 0.7);
}

.slider-arrow-prev {
  left: 1rem;
}

.slider-arrow-next {
  right: 1rem;
}

.slider-dots {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  background: rgba(8, 6, 4, 0.55);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(222, 186, 78, 0.2);
  z-index: 6;
}

.slider-dot {
  width: 0.55rem;
  height: 0.55rem;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.35);
  cursor: pointer;
  transition: all 0.25s ease;
  padding: 0;
}

.slider-dot.active {
  background: var(--color-gold-light);
  transform: scale(1.15);
}

.slider-dot:hover:not(.active) {
  background: rgba(255, 255, 255, 0.65);
}

/* Info side */
.modal-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.modal-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.modal-material {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-gold);
}

.modal-collection {
  font-family: var(--font-body);
  font-size: 0.65rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-accent-light);
  opacity: 0.85;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.modal-collection::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--color-accent);
  box-shadow: 0 0 8px var(--color-accent);
}

.modal-title {
  font-size: 2.5rem;
  font-weight: 400;
  letter-spacing: 0.01em;
  margin-bottom: 1.25rem;
  color: var(--color-text);
  line-height: 1.1;
}

.modal-divider {
  height: 1px;
  background: linear-gradient(
    to right,
    rgba(222, 186, 78, 0.4) 0%,
    rgba(222, 186, 78, 0.15) 35%,
    rgba(16, 185, 129, 0.2) 70%,
    transparent 100%
  );
  margin-bottom: 1.5rem;
}

.modal-desc {
  color: var(--color-text-muted);
  font-size: 1rem;
  line-height: 1.7;
  margin-bottom: 2rem;
  opacity: 0.85;
}

/* Features grid */
.modal-features {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
  margin-bottom: 2rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.85rem 1rem;
  background: rgba(222, 186, 78, 0.03);
  border: 1px solid rgba(222, 186, 78, 0.08);
  border-radius: 4px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.feature::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--color-gold), var(--color-accent));
  opacity: 0;
  transition: opacity 0.3s ease;
}
.feature:hover {
  background: rgba(222, 186, 78, 0.06);
  border-color: rgba(222, 186, 78, 0.2);
}
.feature:hover::before {
  opacity: 1;
}

.feature-icon {
  width: 22px;
  height: 22px;
  color: var(--color-gold);
  flex-shrink: 0;
}

.feature-label {
  font-family: var(--font-body);
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin-bottom: 0.15rem;
  opacity: 0.7;
}

.feature-value {
  font-family: var(--font-body);
  font-size: 0.9rem;
  font-weight: 400;
  color: var(--color-text);
  letter-spacing: 0.01em;
}

/* Footer */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.modal-price-block {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.modal-price {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 400;
  letter-spacing: 0.02em;
  color: var(--color-gold-light);
  line-height: 1;
}

.modal-price-note {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  opacity: 0.6;
}

.modal-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
  background: linear-gradient(135deg, #deba4e, #e8c9a0);
  color: #0a0a0a;
  padding: 1rem 1.75rem;
  border-radius: 999px;
  font-family: var(--font-body);
  font-size: 0.75rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  font-weight: 500;
  transition: all 0.35s ease;
  border: 1px solid transparent;
  position: relative;
  overflow: hidden;
}
.modal-cta::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #e8c9a0, #deba4e);
  opacity: 0;
  transition: opacity 0.35s ease;
}
.modal-cta > * {
  position: relative;
  z-index: 1;
}
.modal-cta:hover {
  box-shadow: 0 12px 30px -10px rgba(222, 186, 78, 0.6);
  transform: translateY(-2px);
}
.modal-cta:hover::before {
  opacity: 1;
}
.modal-cta svg {
  transition: transform 0.35s ease;
}
.modal-cta:hover svg {
  transform: translateX(3px);
}

/* ===========================================
   Specs block (Она / Он, таблица, металлы)
   =========================================== */

.spec-tabs {
  display: inline-flex;
  gap: 0.25rem;
  padding: 0.3rem;
  background: rgba(222, 186, 78, 0.04);
  border: 1px solid rgba(222, 186, 78, 0.12);
  border-radius: 999px;
  margin-bottom: 1.5rem;
}

.spec-tab {
  appearance: none;
  background: transparent;
  border: 0;
  color: var(--color-text-muted);
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  padding: 0.55rem 1.4rem;
  border-radius: 999px;
  cursor: pointer;
  transition: color 0.3s ease, background 0.3s ease;
}

.spec-tab:hover {
  color: var(--color-gold-light);
}

.spec-tab.active {
  background: linear-gradient(135deg, rgba(222, 186, 78, 0.9), rgba(232, 201, 160, 0.9));
  color: #0a0a0a;
  font-weight: 500;
}

.spec-table {
  display: flex;
  flex-direction: column;
  margin: 0 0 2rem;
  padding: 0;
  border-top: 1px solid rgba(222, 186, 78, 0.1);
}

.spec-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.85rem 0;
  border-bottom: 1px solid rgba(222, 186, 78, 0.08);
}

.spec-row dt {
  font-family: var(--font-body);
  font-size: 0.7rem;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  opacity: 0.75;
  margin: 0;
}

.spec-row dd {
  font-family: var(--font-body);
  font-size: 0.95rem;
  color: var(--color-text);
  letter-spacing: 0.01em;
  margin: 0;
  text-align: right;
}

.metals-block {
  margin-bottom: 2rem;
}

.metals-label {
  font-family: var(--font-body);
  font-size: 0.65rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-text-muted);
  opacity: 0.75;
  margin-bottom: 0.9rem;
}

.metals-row {
  display: flex;
  gap: 0.7rem;
  margin-bottom: 0.85rem;
}

.metal-dot {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
  box-shadow:
    inset 0 1px 1px rgba(255, 255, 255, 0.35),
    inset 0 -2px 3px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(222, 186, 78, 0.18),
    0 4px 10px -4px rgba(0, 0, 0, 0.6);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  cursor: help;
}

.metal-dot:hover {
  transform: translateY(-2px) scale(1.08);
  box-shadow:
    inset 0 1px 1px rgba(255, 255, 255, 0.45),
    inset 0 -2px 3px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(222, 186, 78, 0.45),
    0 6px 14px -4px rgba(0, 0, 0, 0.7);
}

.metals-legend {
  font-family: var(--font-body);
  font-size: 0.72rem;
  line-height: 1.6;
  color: var(--color-text-muted);
  opacity: 0.7;
  letter-spacing: 0.02em;
}

/* Mobile responsiveness */
@media (max-width: 900px) {
  .modal-content {
    display: flex;
    flex-direction: column;
    padding: 2rem;
    gap: 2rem;
    border-radius: 4px;
  }

  .modal-image-wrapper {
    width: 100%;
    aspect-ratio: 1/1;
    flex-shrink: 0;
  }

  .slider-arrow {
    width: 2rem;
    height: 2rem;
  }

  .slider-arrow-prev {
    left: 0.6rem;
  }

  .slider-arrow-next {
    right: 0.6rem;
  }

  .modal-info {
    flex-shrink: 0;
    min-width: 0;
  }

  .modal-title {
    font-size: 1.75rem;
  }

  .modal-features {
    grid-template-columns: 1fr;
    gap: 0.85rem;
  }

  .modal-footer {
    flex-direction: column;
    align-items: stretch;
    gap: 1.25rem;
  }

  .modal-cta {
    justify-content: center;
  }
}
</style>
