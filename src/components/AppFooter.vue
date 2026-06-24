<template>
  <footer id="footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="#" class="logo logo-with-icon heading-font uppercase">
            <img :src="logoSrc" alt="Rings Atelier" class="logo-img">
            <span>Rings Atelier</span>
          </a>
          <p class="footer-desc font-light">Rings Atelier — ювелирная мастерская в Санкт-Петербурге. Премиальные мастер-классы по созданию обручальных колец, помолвочных колец и украшений на заказ в самом сердце города.</p>
        </div>
        
        <div class="footer-contact">
          <h4 class="footer-title">Контакты</h4>
          <div class="footer-links">
            <span>Санкт-Петербург, улица Мясная, 20</span>
            <a href="tel:+79990687807">+7 (999) 068‒78‒07</a>
            <span class="hours">Мы работаем для Вас ежедневно с 11:00 до 20:00</span>
          </div>
        </div>

        <div class="footer-social">
          <h4 class="footer-title">Соцсети</h4>
          <div class="footer-links">
            <a href="https://t.me/RingsAtelier" target="_blank" rel="noopener noreferrer">Telegram</a>
            <a href="https://max.ru/u/f9LHodD0cOI2dWqhl4pMfYTZAPNJ5ceh8BRB4mmMt-WKXBfbaTe_78Td_ME" target="_blank" rel="noopener noreferrer">Max</a>
            <a href="https://vk.ru/rings.atelier" target="_blank" rel="noopener noreferrer">ВКонтакте</a>
          </div>
        </div>
      </div>

      <div class="footer-legal">
        <div class="footer-legal-links">
          <RouterLink to="/personal-data">Политика в отношении обработки персональных данных</RouterLink>
          <span class="legal-sep">·</span>
          <RouterLink to="/privacy">Политика конфиденциальности</RouterLink>
          <span class="legal-sep">·</span>
          <RouterLink to="/offer">Публичная оферта</RouterLink>
        </div>
      </div>

      <div class="footer-bottom font-light">
        <span>&copy; 2026 Rings Atelier. Все права защищены.</span>
        <a href="https://whitestudio.tech" target="_blank" rel="noopener noreferrer" class="created-by">
          <span>Created by</span>
          <span class="created-by-name">WhiteStudio</span>
          <svg class="created-by-arrow" width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 11L11 1M11 1H3M11 1V9" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </a>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import logoSrc from '/favicon.svg'
</script>

<style scoped>
.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-links span, .footer-links a {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: var(--color-accent);
}

.hours {
  display: block;
  margin-top: 0;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-left: 2px solid var(--color-accent);
  font-size: 0.8rem !important;
  color: var(--color-text-muted) !important;
}

.footer-legal {
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  padding: 1.5rem 0;
  margin-bottom: 0;
}

.footer-legal-links {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.5rem 0.75rem;
}

.footer-legal-links a {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  letter-spacing: 0.05em;
  transition: color 0.3s ease;
  text-decoration: none;
  position: relative;
}

.footer-legal-links a::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--color-accent);
  transition: width 0.3s ease;
}

.footer-legal-links a:hover {
  color: var(--color-text);
}

.footer-legal-links a:hover::after {
  width: 100%;
}

.legal-sep {
  color: rgba(255, 255, 255, 0.15);
  font-size: 0.75rem;
  user-select: none;
}

.created-by {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: color 0.3s ease;
}

.created-by-name {
  color: var(--color-gold);
  font-weight: 500;
  transition: color 0.3s ease, text-shadow 0.3s ease;
}

.created-by-arrow {
  color: var(--color-text-muted);
  opacity: 0.6;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.created-by:hover {
  color: var(--color-text);
}

.created-by:hover .created-by-name {
  color: var(--color-accent);
  text-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
}

.created-by:hover .created-by-arrow {
  opacity: 1;
  transform: translate(1px, -1px);
}

@media (max-width: 768px) {
  .footer-legal-links {
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }

  .legal-sep {
    display: none;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}

.logo-with-icon {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-img {
  height: 2.5rem;
  width: auto;
  display: block;
}

@media (max-width: 768px) {
  .logo-img {
    height: 2rem;
  }
}
</style>
