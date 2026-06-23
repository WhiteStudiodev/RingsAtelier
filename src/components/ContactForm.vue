<template>
  <section class="contact-section" id="booking">
    <div class="container maxWidth-md">
      <div class="glass-card contact-card" data-reveal>
        <div class="section-header">
          <span class="section-subtitle uppercase tracking-widest">Обратная связь</span>
          <h2 class="section-title heading-font">Записаться в студию</h2>
          <div class="separator"></div>
        </div>
        
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
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Отправка...' : 'Отправить запрос' }}
            </button>
          </div>
          
          <p v-if="submitted" class="success-message">Спасибо за доверие! Мы свяжемся с вами в ближайшее время.</p>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue'

const form = reactive({
  name: '',
  method: 'tg',
  contact: '',
  message: ''
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

// Close dropdown on click outside
if (typeof window !== 'undefined') {
  window.addEventListener('click', (e) => {
    if (selectRef.value && !selectRef.value.contains(e.target)) {
      showDropdown.value = false
    }
  })
}

const isSubmitting = ref(false)
const submitted = ref(false)
const errors = reactive({
  name: '',
  contact: '',
  message: ''
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
}

const handleSubmit = () => {
  // Validate all fields
  validateField('name')
  validateField('contact')
  validateField('message')
  
  if (Object.values(errors).some(e => e !== '')) return

  isSubmitting.value = true
  // Simulate API call
  setTimeout(() => {
    isSubmitting.value = false
    submitted.value = true
    Object.keys(form).forEach(key => form[key] = key === 'method' ? 'tg' : '')
    
    setTimeout(() => {
      submitted.value = false
    }, 5000)
  }, 1500)
}
</script>

<style scoped>
.contact-section {
  padding: 3rem 0;
}

.maxWidth-md {
  max-width: 800px;
  margin: 0 auto;
}

.contact-card {
  padding: 4rem;
  border-radius: 2rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0));
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.contact-form {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
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
  border-right: 2px solid var(--color-accent);
  border-bottom: 2px solid var(--color-accent);
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
  background: var(--color-accent);
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
  gap: 0.75rem;
}

.form-group label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-accent);
}

.form-group input,
.form-group textarea {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  color: white;
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-accent);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 15px rgba(234, 88, 12, 0.2);
}

.form-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: center;
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 640px) {
  .contact-card {
    padding: 2rem;
  }
}
</style>
