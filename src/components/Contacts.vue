<template>
  <section id="contact" class="contacts-section">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Ждём в гости</span>
        <h2 class="section-title heading-font">Контакты и запись</h2>
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
              <input type="text" id="name" v-model="form.name" @blur="validateField('name')" placeholder="Константин">
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
              <textarea id="message" v-model="form.message" @blur="validateField('message')" placeholder="Хочу создать парные обручальные кольца..." rows="4"></textarea>
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
                <a href="tel:+79991234567" class="info-value">+7 (999) 123-45-67</a>
              </div>
              <div class="info-item">
                <span class="info-label">Режим работы</span>
                <span class="info-value">Ежедневно 10:00 — 21:00</span>
                <span class="info-hint">по предварительной записи</span>
              </div>
            </div>

            <div class="socials">
              <a href="#" class="social-link" aria-label="Telegram">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </a>
              <a href="#" class="social-link" aria-label="Messenger Max">
                <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C6.477 2 2 6.03 2 11c0 2.825 1.453 5.344 3.738 7.025C5.1 19.345 4.3 21 4.3 21c3.55 0 6-1.55 6-1.55A10.74 10.74 0 0 0 12 20c5.523 0 10-4.03 10-9s-4.477-9-10-9z"/>
                </svg>
              </a>
              <a href="#" class="social-link" aria-label="VK">
                <svg width="22" height="22" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.684 15.65c-6.19 0-9.752-4.22-9.927-11.23h3.298c.117 5.25 2.508 7.37 4.412 7.82v-7.82h3.13v4.46c1.88-.2 3.856-2.4 4.542-4.46h3.13c-.567 2.66-2.585 4.69-4.004 5.58 1.418.72 3.69 2.51 4.522 5.65h-3.41c-.636-2.22-2.39-3.88-4.437-4.11v4.11h-1.258Z"/>
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
  method: 'tg',
  contact: '',
  message: '',
  consent: false
})

const showDropdown = ref(false)
const selectRef = ref(null)

const contactMethods = [
  { id: 'tg', label: 'Telegram', placeholder: '@username' },
  { id: 'max', label: 'Max', placeholder: 'ID или ссылка...' },
  { id: 'vk', label: 'ВКонтакте', placeholder: 'vk.com/id...' },
  { id: 'phone', label: 'Номер телефона', placeholder: '+7 --- --- -- --' }
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

    if (form.method === 'tg') {
      if (!val.startsWith('@') && !val.includes('t.me/')) {
        errors.contact = 'Никнейм должен начинаться с @'
      }
    } else if (form.method === 'phone') {
      const phoneRegex = /^(\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/
      if (!phoneRegex.test(val)) {
        errors.contact = 'Неверный формат номера'
      }
    } else if (form.method === 'vk') {
      if (!val.includes('vk.com/') && val.length < 3) {
        errors.contact = 'Введите ссылку или ID'
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
  validateField('name')
  validateField('contact')
  validateField('message')
  validateField('consent')

  if (Object.values(errors).some(e => e !== '')) return

  isSubmitting.value = true

  try {
    await submitLead(form)

    submitted.value = true
    Object.keys(form).forEach(key => {
      if (key === 'method') form[key] = 'tg'
      else if (key === 'consent') form[key] = false
      else form[key] = ''
    })

    setTimeout(() => {
      submitted.value = false
    }, 5000)
  } catch (error) {
    console.error('Submit error:', error)
    showToast('Произошла ошибка, попробуйте позже')
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
