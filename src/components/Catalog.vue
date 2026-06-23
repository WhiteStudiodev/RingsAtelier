<template>
  <section id="products">
    <div class="container">
      <div class="section-header catalog-header" data-reveal>
        <h2 class="section-title heading-font catalog-title catalog-title-gold">Примеры изделий</h2>
        <div class="separator"></div>
        <p class="catalog-lead">Все модели — это лишь примеры наших работ. Вы всегда можете изменить дизайн, форму и фактуру, добавить гравировку или воплотить вашу собственную идею в золоте.</p>
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
                :src="item.image"
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
          <span class="show-more-count">{{ catalogItems.length - visibleCount }}</span>
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
                :src="selectedProduct.image"
                :alt="selectedProduct.title"
                class="modal-image"
                decoding="async"
                width="1480"
                height="2048"
              >
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import ring1 from '../../rings/DSC06212.webp'
import ring2 from '../../rings/DSC06247.webp'
import ring3 from '../../rings/DSC06251.webp'
import ring4 from '../../rings/DSC06289.webp'
import ring5 from '../../rings/DSC06323.webp'
import ring6 from '../../rings/DSC06338.webp'
import ring7 from '../../rings/DSC06365.webp'
import ring8 from '../../rings/DSC06381.webp'
import ring9 from '../../rings/DSC06409.webp'
import ring10 from '../../rings/DSC06410.webp'
import ring11 from '../../rings/DSC06441.webp'
import ring12 from '../../rings/DSC06478.webp'
import ring13 from '../../rings/DSC06504.webp'
import ring14 from '../../rings/DSC06531.webp'
import ring15 from '../../rings/DSC06538.webp'
import ring16 from '../../rings/DSC06565.webp'
import ring17 from '../../rings/DSC06579.webp'
import ring18 from '../../rings/DSC06606.webp'
import ring19 from '../../rings/DSC06624.webp'
import ring20 from '../../rings/DSC06646.webp'
import ring21 from '../../rings/DSC06782.webp'
import ring22 from '../../rings/DSC06800.webp'
import ring23 from '../../rings/DSC06803.webp'
import ring24 from '../../rings/DSC06805.webp'
import ring25 from '../../rings/DSC06810.webp'
import ring26 from '../../rings/DSC06812.webp'
import ring27 from '../../rings/DSC06815.webp'
import ring28 from '../../rings/DSC06816.webp'
import ring29 from '../../rings/DSC06821.webp'
import ring30 from '../../rings/DSC06824.webp'
import ring31 from '../../rings/DSC06825.webp'
import ring32 from '../../rings/DSC06827.webp'
import ring33 from '../../rings/DSC06830.webp'
import ring34 from '../../rings/DSC06831.webp'
import ring35 from '../../rings/DSC06834.webp'
import ring36 from '../../rings/DSC06839.webp'
import ring37 from '../../rings/DSC06840.webp'
import ring38 from '../../rings/DSC06843.webp'
import ring39 from '../../rings/DSC06849.webp'
import ring40 from '../../rings/DSC06850.webp'
import ring41 from '../../rings/DSC06853.webp'
import ring42 from '../../rings/DSC06856.webp'
import ring43 from '../../rings/DSC06858.webp'
import ring44 from '../../rings/DSC06863.webp'
import ring45 from '../../rings/DSC06867.webp'
import ring46 from '../../rings/DSC06868.webp'
import ring47 from '../../rings/DSC06870.webp'
import ring48 from '../../rings/DSC06872.webp'
import ring49 from '../../rings/DSC06876.webp'
import ring50 from '../../rings/DSC06878.webp'
import ring51 from '../../rings/DSC06879.webp'
import ring52 from '../../rings/DSC06880.webp'
import ring53 from '../../rings/DSC06882.webp'

const router = useRouter()
const selectedProduct = ref(null)
const activeSpecTab = ref('female')

const openModal = (item) => {
  selectedProduct.value = item
  activeSpecTab.value = 'female'
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  selectedProduct.value = null
  document.body.style.overflow = ''
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
const visibleItems = computed(() => catalogItems.slice(0, visibleCount.value))
const hasMore = computed(() => visibleCount.value < catalogItems.length)
const showMore = () => {
  visibleCount.value = Math.min(visibleCount.value + VISIBLE_STEP, catalogItems.length)
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
    desc: 'Прямые обручальные кольца с лунной фактурой.',
    price: 'от 89 578 ₽',
    material: 'Металл на выбор',
    image: ring6,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с лунной фактурой в белом золоте.',
      female: { size: '16', width: '4 мм' },
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
    title: 'Полосатые шайбы',
    desc: 'Прямые шайбы с контрастными полосками и акцентным бриллиантом.',
    price: 'от 82 654 ₽',
    material: 'Металл на выбор',
    image: ring14,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с полосками и акцентным бриллиантом в белом золоте.',
      female: { size: '16', width: '2,5 мм', diamonds: 'Круг · 0,015 ct' },
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
    title: 'Зимний лёд',
    desc: 'Прямые шайбы с фактурой зимнего льда.',
    price: 'от 79 453 ₽',
    material: 'Металл на выбор',
    image: ring2,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с фактурой «Зимний лёд» в белом золоте.',
      female: { size: '17', width: '3,5 мм' },
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
    title: 'Комбинированные шайбы',
    desc: 'Шайбы с вставками из двух золотых оттенков.',
    price: 'от 98 658 ₽',
    material: 'Металл на выбор',
    image: ring13,
    bestseller: false,
    specs: {
      style: 'Комбинированные обручальные кольца «шайбы» со вставками в белом и жёлтом золоте.',
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
    price: 'от 85 652 ₽',
    material: 'Металл на выбор',
    image: ring3,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с фактурой «Горы» в белом золоте.',
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
    title: 'Полусферы «Ямчатая»',
    desc: 'Полусферы с матовой ямчатой фактурой.',
    price: 'от 81 582 ₽',
    material: 'Металл на выбор',
    image: ring18,
    bestseller: false,
    specs: {
      style: 'Обручальные кольца полусферы с матовой ямчатой фактурой в белом золоте.',
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
    title: 'Сатиновые шайбы',
    desc: 'Шайбы с перекрёстной сатиновой матовкой и глянцевыми краями.',
    price: 'от 101 600 ₽',
    material: 'Металл на выбор',
    image: ring9,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с перекрёстной сатиновой матовкой и глянцевыми краями в белом золоте.',
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
    price: 'от 82 654 ₽',
    material: 'Металл на выбор',
    image: ring7,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с полосками в белом золоте.',
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
    price: 'от 99 785 ₽',
    material: 'Металл на выбор',
    image: ring1,
    bestseller: false,
    specs: {
      style: 'Глянцевые обручальные кольца «шайбы» с прорезью в белом золоте.',
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
    desc: 'Прямые шайбы с глянцевой и матовой поверхностью и бриллиантом.',
    price: 'от 117 689 ₽',
    material: 'Металл на выбор',
    image: ring15,
    bestseller: false,
    specs: {
      style: 'Прямые обручальные кольца «шайбы» с глянцевой и матовой поверхностью и бриллиантом 2 мм в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,012 ct' },
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
    title: 'Перекрут «Бесконечность»',
    desc: 'Обручальные кольца перекрут «Бесконечность» в белом золоте.',
    price: 'от 81 256 ₽',
    material: 'Металл на выбор',
    image: ring10,
    bestseller: false,
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
    title: 'Полусферы «Глянцевые ямки»',
    desc: 'Полусферы с глянцевой ямчатой фактурой в белом золоте.',
    price: 'от 76 845 ₽',
    material: 'Металл на выбор',
    image: ring4,
    bestseller: false,
    specs: {
      style: 'Обручальные кольца полусферы с глянцевой ямчатой фактурой в белом золоте.',
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
    desc: 'Кольца с комфортной посадкой, матовой и глянцевой поверхностью, прорезью и бриллиантами.',
    price: 'от 135 478 ₽',
    material: 'Металл на выбор',
    image: ring5,
    bestseller: false,
    specs: {
      style: 'Обручальные кольца с комфортной посадкой, матовой и глянцевой поверхностью, прорезью и вставками бриллиантов 1,5 мм в белом золоте.',
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
    desc: 'Обручальные кольца с фактурой «Грани» и бриллиантами в белом золоте.',
    price: 'от 121 943 ₽',
    material: 'Металл на выбор',
    image: ring8,
    bestseller: false,
    specs: {
      style: 'Обручальные кольца с фактурой «Грани» и бриллиантами 1,25 мм в белом золоте.',
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
    price: 'от 89 547 ₽',
    material: 'Металл на выбор',
    image: ring19,
    bestseller: false,
    specs: {
      style: 'Прямые глянцевые обручальные кольца «шайбы» с продольной фактурой «Волна» в белом золоте.',
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
    desc: 'Составные двухцветные матовые шайбы с глянцевыми краями и бриллиантами.',
    price: 'от 124 653 ₽',
    material: 'Металл на выбор',
    image: ring12,
    bestseller: false,
    specs: {
      style: 'Составные двухцветные матовые обручальные кольца «шайбы» с глянцевыми краями и бриллиантами 1,5 мм в белом и красном золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,19 ct' },
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
    desc: 'Комбинированные двухцветные шайбы с выемками и бриллиантами открытой дорожкой.',
    price: 'от 121 859 ₽',
    material: 'Металл на выбор',
    image: ring17,
    bestseller: false,
    specs: {
      style: 'Комбинированные двухцветные обручальные кольца «шайбы» с выемками и вставками бриллиантов открытой дорожкой 2 мм.',
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
    title: 'Шайба',
    desc: 'Прямой профиль с сатиновой матовкой и глянцевыми фасками. Парные.',
    price: '78 000 ₽',
    material: 'Пара · Бриллианты',
    image: ring11,
    bestseller: false,
    specs: {
      style: 'Прямой профиль «шайба». Сатиновая продольная матовка с глянцевыми фасками. Женское — с дорожкой бриллиантов огранки «Круг», мужское — гладкое глянцевое.',
      female: {
        size: '16',
        width: '3 мм',
        diamonds: 'Круг · 0,013 ct'
      },
      male: {
        size: '18',
        width: '5 мм'
      },
      metals: [
        { label: 'Серебро 925',           color: '#C7C9CE' },
        { label: 'Белое золото 585/750',  color: '#E4E6EA' },
        { label: 'Жёлтое золото 585/750', color: '#E5C56A' },
        { label: 'Красное золото 585/750',color: '#C8775A' },
        { label: 'Розовое золото 585/750',color: '#E5B6A6' },
        { label: 'Платина 950',           color: '#D6D8DC' }
      ]
    }
  },
  {
    title: 'Матовые шайбы «Волна»',
    desc: 'Прямые матовые шайбы с глянцевой фактурой «Волна».',
    price: 'от 90 926 ₽',
    material: 'Металл на выбор',
    image: ring20,
    bestseller: false,
    specs: {
      style: 'Прямые матовые обручальные кольца «шайбы» с глянцевой фактурой «Волна» в белом золоте.',
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
    desc: 'Гладкие шайбы с фасками и бриллиантами 2 мм в белом золоте.',
    price: 'от 108 685 ₽',
    material: 'Металл на выбор',
    image: ring16,
    bestseller: false,
    specs: {
      style: 'Гладкие обручальные кольца «шайбы» с фасками и бриллиантами 2 мм в белом золоте.',
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
    title: 'Помолвочное кольцо с бриллиантом',
    desc: 'Помолвочное кольцо с крупным центральным бриллиантом.',
    price: 'от 125 000 ₽',
    material: 'Металл на выбор',
    image: ring21,
    bestseller: false,
    specs: {
      style: 'Помолвочное кольцо с бриллиантом в белом золоте.',
      female: { size: '16', width: '2 мм', diamonds: 'Круг · 0,5 ct' },
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
    title: 'Тонкая дорожка с бриллиантами',
    desc: 'Тонкое обручальное кольцо с дорожкой мелких бриллиантов.',
    price: 'от 98 000 ₽',
    material: 'Металл на выбор',
    image: ring22,
    bestseller: false,
    specs: {
      style: 'Тонкая дорожка с бриллиантами в белом золоте.',
      female: { size: '16', width: '2 мм', diamonds: 'Круг · 0,12 ct' },
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
    title: 'Двухцветная шайба с дорожкой',
    desc: 'Двухцветная обручальная шайба с дорожкой бриллиантов.',
    price: 'от 115 000 ₽',
    material: 'Металл на выбор',
    image: ring23,
    bestseller: false,
    specs: {
      style: 'Двухцветная шайба с дорожкой в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,18 ct' },
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
    title: 'Широкая шайба с бриллиантами',
    desc: 'Широкая обручальная шайба с бриллиантовой вставкой.',
    price: 'от 118 000 ₽',
    material: 'Металл на выбор',
    image: ring24,
    bestseller: false,
    specs: {
      style: 'Широкая шайба с бриллиантами в белом золоте.',
      female: { size: '16', width: '4 мм', diamonds: 'Круг · 0,21 ct' },
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
    title: 'Минималистичная дорожка с бриллиантами',
    desc: 'Тонкое кольцо с минималистичной дорожкой бриллиантов.',
    price: 'от 92 000 ₽',
    material: 'Металл на выбор',
    image: ring25,
    bestseller: false,
    specs: {
      style: 'Минималистичная дорожка с бриллиантами в белом золоте.',
      female: { size: '16', width: '2 мм', diamonds: 'Круг · 0,09 ct' },
      male:   { size: '18', width: '2,5 мм' },
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
    title: 'Шайба с геометрической фактурой',
    desc: 'Обручальная шайба с контрастной геометрической огранкой.',
    price: 'от 88 000 ₽',
    material: 'Металл на выбор',
    image: ring26,
    bestseller: false,
    specs: {
      style: 'Шайба с геометрической фактурой в белом золоте.',
      female: { size: '16', width: '4 мм', },
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
    title: 'Шайба с текстурой коры дерева',
    desc: 'Обручальная шайба с фактурой, напоминающей кору дерева.',
    price: 'от 86 000 ₽',
    material: 'Металл на выбор',
    image: ring27,
    bestseller: false,
    specs: {
      style: 'Шайба с текстурой коры дерева в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Шайба с одиночным бриллиантом',
    desc: 'Обручальная шайба с центральным бриллиантом.',
    price: 'от 108 000 ₽',
    material: 'Металл на выбор',
    image: ring28,
    bestseller: false,
    specs: {
      style: 'Шайба с одиночным бриллиантом в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,04 ct' },
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
    title: 'Шайба с волнистой фактурой',
    desc: 'Обручальная шайба с волнистой текстурой поверхности.',
    price: 'от 84 000 ₽',
    material: 'Металл на выбор',
    image: ring29,
    bestseller: false,
    specs: {
      style: 'Шайба с волнистой фактурой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Шайба с диагональной насечкой',
    desc: 'Обручальная шайба с диагональной алмазной насечкой.',
    price: 'от 89 000 ₽',
    material: 'Металл на выбор',
    image: ring30,
    bestseller: false,
    specs: {
      style: 'Шайба с диагональной насечкой в белом золоте.',
      female: { size: '16', width: '3,5 мм', },
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
    title: 'Матовая шайба с глянцевым центром',
    desc: 'Матовая обручальная шайба с глянцевой центральной полосой.',
    price: 'от 94 000 ₽',
    material: 'Металл на выбор',
    image: ring31,
    bestseller: false,
    specs: {
      style: 'Матовая шайба с глянцевым центром в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Широкая матовая шайба',
    desc: 'Широкая матовая обручальная шайба с гладкой поверхностью.',
    price: 'от 91 000 ₽',
    material: 'Металл на выбор',
    image: ring32,
    bestseller: false,
    specs: {
      style: 'Широкая матовая шайба в белом золоте.',
      female: { size: '16', width: '4 мм', },
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
    title: 'Тонкая шайба с микро-бриллиантами',
    desc: 'Тонкое кольцо с микро-бриллиантами по всему ободку.',
    price: 'от 96 000 ₽',
    material: 'Металл на выбор',
    image: ring33,
    bestseller: false,
    specs: {
      style: 'Тонкая шайба с микро-бриллиантами в белом золоте.',
      female: { size: '16', width: '2 мм', diamonds: 'Круг · 0,11 ct' },
      male:   { size: '18', width: '2,5 мм' },
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
    title: 'Шайба с двойной дорожкой камней',
    desc: 'Обручальная шайба с двумя дорожками бриллиантов.',
    price: 'от 122 000 ₽',
    material: 'Металл на выбор',
    image: ring34,
    bestseller: false,
    specs: {
      style: 'Шайба с двойной дорожкой камней в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,24 ct' },
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
    title: 'Шайба с перекрёстной сатиновкой',
    desc: 'Обручальная шайба с перекрёстной сатиновой матовкой.',
    price: 'от 87 000 ₽',
    material: 'Металл на выбор',
    image: ring35,
    bestseller: false,
    specs: {
      style: 'Шайба с перекрёстной сатиновкой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Обручальное кольцо с центральным бриллиантом',
    desc: 'Классическое обручальное кольцо с центральным бриллиантом.',
    price: 'от 112 000 ₽',
    material: 'Металл на выбор',
    image: ring36,
    bestseller: false,
    specs: {
      style: 'Обручальное кольцо с центральным бриллиантом в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,05 ct' },
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
    title: 'Шайба с рустикальной фактурой',
    desc: 'Обручальная шайба с рустикальной текстурой металла.',
    price: 'от 85 000 ₽',
    material: 'Металл на выбор',
    image: ring37,
    bestseller: false,
    specs: {
      style: 'Шайба с рустикальной фактурой в белом золоте.',
      female: { size: '16', width: '3,5 мм', },
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
    title: 'Глянцевая шайба с выемкой',
    desc: 'Глянцевая обручальная шайба с декоративной выемкой.',
    price: 'от 90 000 ₽',
    material: 'Металл на выбор',
    image: ring38,
    bestseller: false,
    specs: {
      style: 'Глянцевая шайба с выемкой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Шайба с дорожкой и фасками',
    desc: 'Обручальная шайба с дорожкой бриллиантов и фасками.',
    price: 'от 105 000 ₽',
    material: 'Металл на выбор',
    image: ring39,
    bestseller: false,
    specs: {
      style: 'Шайба с дорожкой и фасками в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,16 ct' },
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
    title: 'Миниатюрная дорожка с бриллиантами',
    desc: 'Миниатюрное кольцо с тонкой дорожкой бриллиантов.',
    price: 'от 88 000 ₽',
    material: 'Металл на выбор',
    image: ring40,
    bestseller: false,
    specs: {
      style: 'Миниатюрная дорожка с бриллиантами в белом золоте.',
      female: { size: '16', width: '1,8 мм', diamonds: 'Круг · 0,07 ct' },
      male:   { size: '18', width: '2,5 мм' },
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
    title: 'Шайба с вертикальной шлифовкой',
    desc: 'Обручальная шайба с вертикальной сатиновой шлифовкой.',
    price: 'от 83 000 ₽',
    material: 'Металл на выбор',
    image: ring41,
    bestseller: false,
    specs: {
      style: 'Шайба с вертикальной шлифовкой в белом золоте.',
      female: { size: '16', width: '3,5 мм', },
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
    title: 'Двухцветная шайба с канавкой',
    desc: 'Двухцветная обручальная шайба с декоративной канавкой.',
    price: 'от 102 000 ₽',
    material: 'Металл на выбор',
    image: ring42,
    bestseller: false,
    specs: {
      style: 'Двухцветная шайба с канавкой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Шайба с бриллиантовой пластиной',
    desc: 'Обручальная шайба с вставкой из мелких бриллиантов.',
    price: 'от 110 000 ₽',
    material: 'Металл на выбор',
    image: ring43,
    bestseller: false,
    specs: {
      style: 'Шайба с бриллиантовой пластиной в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,14 ct' },
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
    title: 'Фактурная шайба с полированными гранями',
    desc: 'Обручальная шайба с фактурной поверхностью и полированными гранями.',
    price: 'от 93 000 ₽',
    material: 'Металл на выбор',
    image: ring44,
    bestseller: false,
    specs: {
      style: 'Фактурная шайба с полированными гранями в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Шайба с горизонтальной насечкой',
    desc: 'Обручальная шайба с горизонтальной алмазной насечкой.',
    price: 'от 82 000 ₽',
    material: 'Металл на выбор',
    image: ring45,
    bestseller: false,
    specs: {
      style: 'Шайба с горизонтальной насечкой в белом золоте.',
      female: { size: '16', width: '3,5 мм', },
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
    title: 'Широкая матовая шайба с глянцевыми краями',
    desc: 'Широкая матовая шайба с глянцевыми скошенными краями.',
    price: 'от 99 000 ₽',
    material: 'Металл на выбор',
    image: ring46,
    bestseller: false,
    specs: {
      style: 'Широкая матовая шайба с глянцевыми краями в белом золоте.',
      female: { size: '16', width: '4 мм', },
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
    title: 'Тонкая шайба с центральным камнем',
    desc: 'Тонкое обручальное кольцо с центральным бриллиантом.',
    price: 'от 104 000 ₽',
    material: 'Металл на выбор',
    image: ring47,
    bestseller: false,
    specs: {
      style: 'Тонкая шайба с центральным камнем в белом золоте.',
      female: { size: '16', width: '2 мм', diamonds: 'Круг · 0,03 ct' },
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
    title: 'Шайба с двойной текстурой',
    desc: 'Обручальная шайба с сочетанием матовой и глянцевой текстуры.',
    price: 'от 95 000 ₽',
    material: 'Металл на выбор',
    image: ring48,
    bestseller: false,
    specs: {
      style: 'Шайба с двойной текстурой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Глянцевая шайба с боковой дорожкой',
    desc: 'Глянцевая обручальная шайба с боковой дорожкой бриллиантов.',
    price: 'от 116 000 ₽',
    material: 'Металл на выбор',
    image: ring49,
    bestseller: false,
    specs: {
      style: 'Глянцевая шайба с боковой дорожкой в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,19 ct' },
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
    title: 'Шайба с мелкой алмазной насечкой',
    desc: 'Обручальная шайба с мелкой алмазной насечкой по всей поверхности.',
    price: 'от 81 000 ₽',
    material: 'Металл на выбор',
    image: ring50,
    bestseller: false,
    specs: {
      style: 'Шайба с мелкой алмазной насечкой в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
    title: 'Двухцветная шайба с бриллиантами',
    desc: 'Двухцветная обручальная шайба с дорожкой бриллиантов.',
    price: 'от 120 000 ₽',
    material: 'Металл на выбор',
    image: ring51,
    bestseller: false,
    specs: {
      style: 'Двухцветная шайба с бриллиантами в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,22 ct' },
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
    title: 'Шайба с волнами и микро-бриллиантами',
    desc: 'Обручальная шайба с волнообразной фактурой и микро-бриллиантами.',
    price: 'от 128 000 ₽',
    material: 'Металл на выбор',
    image: ring52,
    bestseller: false,
    specs: {
      style: 'Шайба с волнами и микро-бриллиантами в белом золоте.',
      female: { size: '16', width: '3 мм', diamonds: 'Круг · 0,13 ct' },
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
    title: 'Матовая шайба с глянцевыми фасками',
    desc: 'Матовая обручальная шайба с глянцевыми скошенными фасками.',
    price: 'от 97 000 ₽',
    material: 'Металл на выбор',
    image: ring53,
    bestseller: false,
    specs: {
      style: 'Матовая шайба с глянцевыми фасками в белом золоте.',
      female: { size: '16', width: '3 мм', },
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
  height: 100%;
  transform: rotateX(var(--tilt-x)) rotateY(var(--tilt-y));
  transform-style: preserve-3d;
  transition: transform 0.15s ease-out;
  will-change: transform;
}

.catalog-card:not(:hover) .catalog-card-inner {
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

/* === Image area === */
.catalog-card :deep(.catalog-img) {
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
}

.catalog-card:hover :deep(.catalog-img) {
  box-shadow:
    0 1px 0 0 rgba(222, 186, 78, 0.15) inset,
    0 18px 40px -10px rgba(0, 0, 0, 0.7),
    0 0 0 1px rgba(222, 186, 78, 0.15);
}

.catalog-card :deep(.catalog-img img) {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
    grid-template-columns: 1fr;
    padding: 2rem;
    gap: 2rem;
    border-radius: 4px;
  }

  .modal-image-wrapper {
    aspect-ratio: 1/1;
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
