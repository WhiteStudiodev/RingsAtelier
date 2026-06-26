<template>
  <section id="contact" class="contacts-section">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Ждём в гости</span>
        <h2 class="section-title heading-font">Запись на ювелирный мастер-класс в Спб</h2>
        <div class="separator"></div>
      </div>

      <div class="contacts-layout">
        <!-- LEFT: Form -->
        <div class="form-card glass-card" data-reveal>
          <h3 class="block-title heading-font">Оставить заявку</h3>
          <p class="block-subtitle font-light">Свяжемся в ближайшее время и подберём удобную дату.</p>

          <form @submit.prevent="handleSubmit" class="contact-form body-font">
            <div class="form-group" :class="{ 'has-error': errors.name }">
              <label for="name">Ваше имя</label>
              <input type="text" id="name" v-model="form.name" placeholder="Имя">
              <span v-if="errors.name" class="error-text">{{ errors.name }}</span>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.contact }">
              <label>Способ связи</label>
              <div class="custom-select" ref="selectRef">
                <button type="button" class="select-trigger" @click="showDropdown = !showDropdown">
                  <span>{{ contactMethods.find(m => m.id === form.method).label }}</span>
                  <i class="arrow" :class="{ open: showDropdown }"></i>
                </button>

                <Transition name="slide-up">
                  <div v-if="showDropdown" class="select-dropdown glass-panel">
                    <div v-for="method in contactMethods"
                         :key="method.id"
                         class="select-option"
                         @click="selectMethod(method.id)">
                      {{ method.label }}
                    </div>
                  </div>
                </Transition>
              </div>

              <input
                v-if="form.method"
                type="text"
                v-model="form.contact"
                @blur="validateField('contact')"
                :placeholder="contactMethods.find(m => m.id === form.method).placeholder"
                class="method-input"
              >
              <span v-if="errors.contact" class="error-text">{{ errors.contact }}</span>
            </div>

            <div class="form-group" :class="{ 'has-error': errors.message }">
              <label for="message">Пара слов о вашей идее</label>
              <textarea id="message" v-model="form.message" placeholder="Хочу создать парные обручальные кольца..." rows="4"></textarea>
              <span v-if="errors.message" class="error-text">{{ errors.message }}</span>
            </div>

            <div class="form-group consent-group" :class="{ 'has-error': errors.consent }">
              <label class="consent-label">
                <input
                  type="checkbox"
                  v-model="form.consent"
                  @change="validateField('consent')"
                  class="consent-checkbox"
                >
                <span class="consent-text">
                  Я согласен(а) с <router-link to="/personal-data" class="consent-link">политикой обработки персональных данных</router-link>
                </span>
              </label>
              <span v-if="errors.consent" class="error-text">{{ errors.consent }}</span>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                {{ isSubmitting ? 'Отправка...' : 'Отправить запрос' }}
              </button>
            </div>

            <p v-if="submitted" class="success-message">Спасибо за доверие! Мы свяжемся с вами в ближайшее время.</p>
          </form>
        </div>

        <!-- RIGHT: Info + Map stacked -->
        <div class="contacts-side">
          <div class="info-card glass-card" data-reveal data-reveal-delay="1">
            <h3 class="block-title heading-font">Студия Rings Atelier</h3>
            <p class="info-address">г. Санкт-Петербург,<br>улица Мясная, 20</p>

            <div class="info-row">
              <div class="info-item">
                <span class="info-label">Телефон</span>
                <a href="tel:+79990687807" class="info-value">+7 (999) 068‒78‒07</a>
              </div>
              <div class="info-item">
                <span class="info-label">Режим работы</span>
                <span class="info-value">Ежедневно 10:00 — 21:00</span>
                <span class="info-hint">по предварительной записи</span>
              </div>
            </div>

            <div class="socials">
              <a href="https://t.me/RingsAtelier" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="Telegram">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.161c-.18 1.897-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635.099-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.019.472z"/>
                </svg>
              </a>
              <a href="https://max.ru/u/f9LHodD0cOI2dWqhl4pMfYTZAPNJ5ceh8BRB4mmMt-WKXBfbaTe_78Td_ME" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="Max">
                <svg width="22" height="22" viewBox="0 0 48 48" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15.63 40.465c8.083 7.193 27.86-1.166 27.783-15.85C43.36 14.546 35.107 4.59 24.873 4.5c-9.538-.083-19.648 5.962-20.23 17.767-.172 3.515 0 8.859 1.231 11.73 2.335 6.7.113 8.477 2.804 9.328q3.617.9 6.953-2.861z"/>
                </svg>
              </a>
              <a href="https://vk.ru/rings.atelier" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="ВКонтакте">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15.684 0H8.316C1.592 0 0 1.592 0 8.316v7.368C0 22.408 1.592 24 8.316 24h7.368C22.41 24 24 22.408 24 15.684V8.316C24 1.592 22.41 0 15.684 0zm3.692 17.123h-1.744c-.66 0-.864-.525-2.05-1.727-1.033-1-1.49-1.135-1.744-1.135-.356 0-.458.102-.458.593v1.575c0 .424-.135.678-1.253.678-1.846 0-3.896-1.118-5.335-3.202C4.624 10.857 4 8.673 4 8.22c0-.254.102-.491.593-.491h1.744c.44 0 .61.203.78.677.863 2.49 2.303 4.675 2.896 4.675.22 0 .322-.102.322-.66V9.721c-.068-1.186-.695-1.287-.695-1.71 0-.203.17-.407.44-.407h2.744c.373 0 .508.203.508.643v3.473c0 .372.17.508.271.508.22 0 .407-.136.813-.542 1.254-1.406 2.151-3.574 2.151-3.574.119-.254.322-.491.763-.491h1.744c.525 0 .644.27.525.643-.22 1.017-2.354 4.031-2.354 4.031-.186.305-.254.44 0 .78.186.254.796.779 1.203 1.253.745.847 1.32 1.558 1.473 2.05.17.49-.085.744-.576.744z"/>
                </svg>
              </a>
            </div>
          </div>

          <div class="map-wrapper glass-card" data-reveal data-reveal-delay="2">
            <iframe
              src="https://yandex.ru/map-widget/v1/?z=16&ol=biz&oid=243740413465"
              width="100%"
              height="100%"
              frameborder="0"
              allowfullscreen="true"
              loading="lazy"
            ></iframe>
          </div>
        </div>
      </div>
    </div>

    <Transition name="toast">
      <div v-if="toast.show" class="toast" :class="toast.type">
        {{ toast.message }}
      </div>
    </Transition>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { submitLead } from '../services/api.js'

const form = reactive({
  name: '',
  method: 'phone',
  contact: '',
  message: '',
  consent: false
})

const showDropdown = ref(false)
const selectRef = ref(null)

const contactMethods = [
  { id: 'phone', label: 'Номер телефона', placeholder: '+7 --- --- -- --' },
  { id: 'tg', label: 'Telegram', placeholder: '+7 --- --- -- --' },
  { id: 'max', label: 'Max', placeholder: '+7 --- --- -- --' },
  { id: 'vk', label: 'ВКонтакте', placeholder: 'vk.com/id...' }
]

const selectMethod = (id) => {
  form.method = id
  form.contact = ''
  showDropdown.value = false
}

if (typeof window !== 'undefined') {
  window.addEventListener('click', (e) => {
    if (selectRef.value && !selectRef.value.contains(e.target)) {
      showDropdown.value = false
    }
  })
}

const isSubmitting = ref(false)
const submitted = ref(false)
const toast = reactive({
  show: false,
  message: '',
  type: 'error',
  timer: null
})
const errors = reactive({
  name: '',
  contact: '',
  message: '',
  consent: ''
})

const validateField = (field) => {
  errors[field] = ''

  if (field === 'name') {
    if (!form.name.trim()) errors.name = 'Пожалуйста, введите имя'
    else if (form.name.trim().length < 2) errors.name = 'Имя слишком короткое'
  }

  if (field === 'contact') {
    const val = form.contact.trim()
    if (!val) {
      errors.contact = 'Обязательное поле'
      return
    }

    if (form.method === 'vk') {
      if (!val.includes('vk.com/') && val.length < 3) {
        errors.contact = 'Введите ссылку или ID'
      }
    } else {
      const phoneRegex = /^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/
      if (!phoneRegex.test(val)) {
        errors.contact = 'Неверный формат номера'
      }
    }
  }

  if (field === 'message') {
    if (!form.message.trim()) errors.message = 'Напишите хотя бы пару слов'
  }

  if (field === 'consent') {
    if (!form.consent) errors.consent = 'Необходимо согласие на обработку персональных данных'
  }
}

const showToast = (message, type = 'error') => {
  toast.message = message
  toast.type = type
  toast.show = true
  if (toast.timer) clearTimeout(toast.timer)
  toast.timer = setTimeout(() => {
    toast.show = false
  }, 4000)
}

const handleSubmit = async () => {
  validateField('contact')
  validateField('consent')

  if (Object.values(errors).some(e => e !== '')) return

  isSubmitting.value = true

  try {
    await submitLead(form)
    submitted.value = true
    showToast('Спасибо за доверие! Мы свяжемся с вами в ближайшее время.', 'success')

    form.name = ''
    form.contact = ''
    form.message = ''
    form.consent = false
    form.method = 'phone'

    setTimeout(() => {
      submitted.value = false
    }, 5000)
  } catch (error) {
    showToast(error.message || 'Не удалось отправить заявку. Попробуйте ещё раз.', 'error')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.contacts-section {
  padding: 5rem 0;
}

.contacts-layout {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  gap: 2rem;
  margin-top: 3rem;
  align-items: stretch;
}

.contacts-side {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Block Headers */
.block-title {
  font-size: 1.6rem;
  color: var(--color-text);
  margin: 0 0 0.5rem;
}

.block-subtitle {
  font-size: 0.95rem;
  color: var(--color-text-muted);
  margin: 0 0 2rem;
}

/* Form card */
.form-card {
  padding: 2.75rem;
  display: flex;
  flex-direction: column;
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

/* Info card */
.info-card {
  padding: 2rem 2.25rem;
}

.info-address {
  font-size: 1.1rem;
  margin: 0 0 1.5rem;
  line-height: 1.5;
  color: var(--color-gold-light);
}

.info-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.info-label {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--color-text-muted);
}

.info-value {
  font-size: 1rem;
  color: var(--color-text);
  text-decoration: none;
  transition: color 0.3s ease;
}

a.info-value:hover {
  color: var(--color-gold);
}

.info-hint {
  font-size: 0.78rem;
  color: var(--color-text-muted);
}

.socials {
  display: flex;
  gap: 0.75rem;
  padding-top: 1.25rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.social-link {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  color: var(--color-text);
  background: rgba(255, 255, 255, 0.04);
}

.social-link:hover {
  transform: translateY(-3px);
  color: #fff;
}

.social-link:nth-child(1):hover { background: #2AABEE; border-color: #2AABEE; }
.social-link:nth-child(2):hover { background: #168ACD; border-color: #168ACD; }
.social-link:nth-child(3):hover { background: #0077FF; border-color: #0077FF; }

/* Map */
.map-wrapper {
  flex: 1;
  min-height: 280px;
  padding: 0;
  overflow: hidden;
  border-radius: 1.5rem;
}

.map-wrapper iframe {
  width: 100%;
  height: 100%;
  display: block;
  outline: none;
  border: none;
  filter: invert(90%) hue-rotate(180deg) brightness(90%) contrast(110%);
  transition: filter 0.5s ease;
}

.map-wrapper:hover iframe {
  filter: invert(90%) hue-rotate(180deg) brightness(100%) contrast(115%);
}

/* Custom Select */
.custom-select {
  position: relative;
  margin-bottom: 0.5rem;
}

.select-trigger {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  color: white;
  text-align: left;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.select-trigger:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

.arrow {
  width: 10px;
  height: 10px;
  border-right: 2px solid var(--color-gold);
  border-bottom: 2px solid var(--color-gold);
  transform: rotate(45deg);
  transition: all 0.3s ease;
  margin-bottom: 4px;
}

.arrow.open {
  transform: rotate(-135deg);
  margin-bottom: -4px;
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  right: 0;
  background: rgba(2, 44, 34, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  overflow: hidden;
  z-index: 100;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.select-option {
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-option:hover {
  background: var(--color-gold);
  color: var(--color-bg);
}

.method-input {
  animation: slideInInput 0.4s ease;
}

@keyframes slideInInput {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s ease;
}
.slide-up-enter-from, .slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.form-group label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--color-gold);
}

.form-group input:not(.consent-checkbox),
.form-group textarea {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.9rem 1.25rem;
  border-radius: 1rem;
  color: white;
  font-family: inherit;
  font-size: 0.98rem;
  transition: all 0.3s ease;
}

.form-group input:not(.consent-checkbox):focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-gold);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 0 15px rgba(212, 165, 116, 0.15);
}

.form-actions {
  margin-top: 0.5rem;
}

.form-actions .btn {
  width: 100%;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-text {
  color: #f87171;
  font-size: 0.75rem;
  margin-top: 0.25rem;
  animation: slideIn 0.3s ease;
}

.has-error input,
.has-error textarea {
  border-color: #f87171 !important;
  box-shadow: 0 0 10px rgba(248, 113, 113, 0.1);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.success-message {
  text-align: center;
  color: #34d399;
  font-size: 0.9rem;
  margin-top: 1rem;
  animation: fadeIn 0.5s ease;
}

.consent-group {
  gap: 0.25rem;
}

.consent-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.consent-checkbox {
  appearance: none;
  -webkit-appearance: none;
  width: 0.875rem;
  height: 0.875rem;
  min-width: 0.875rem;
  padding: 0;
  margin: 0;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 0.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  box-sizing: border-box;
}

.consent-checkbox:checked {
  background: var(--color-gold);
  border-color: var(--color-gold);
}

.consent-checkbox:checked::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 45%;
  width: 0.2rem;
  height: 0.4rem;
  border: solid var(--color-bg);
  border-width: 0 1.5px 1.5px 0;
  transform: translate(-50%, -50%) rotate(45deg);
}

.consent-checkbox:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(212, 165, 116, 0.3);
}

.consent-text {
  font-size: 0.75rem;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.75);
  text-transform: none;
  letter-spacing: normal;
}

.consent-link {
  color: var(--color-gold);
  text-decoration: underline;
  text-underline-offset: 0.15em;
  transition: opacity 0.2s ease;
}

.consent-link:hover {
  opacity: 0.8;
}

.has-error .consent-checkbox {
  border-color: #f87171;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1024px) {
  .contacts-layout {
    grid-template-columns: 1fr;
  }
  .map-wrapper {
    min-height: 380px;
  }
}

@media (max-width: 640px) {
  .form-card { padding: 2rem 1.5rem; }
  .info-card { padding: 1.75rem; }
  .info-row { grid-template-columns: 1fr; gap: 1.25rem; }
}

/* Toast notification */
.toast {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  z-index: 1000;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  background: rgba(2, 44, 34, 0.95);
  border: 1px solid rgba(248, 113, 113, 0.4);
  color: #f87171;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(10px);
  font-size: 0.9rem;
  max-width: 320px;
  pointer-events: none;
}

.toast.success {
  border-color: rgba(52, 211, 153, 0.4);
  color: #34d399;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 640px) {
  .toast {
    left: 1.5rem;
    right: 1.5rem;
    bottom: 1.5rem;
    max-width: none;
  }
}
</style>
