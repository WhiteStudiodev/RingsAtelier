<template>
  <header class="glass-panel">
    <RouterLink to="/" class="logo heading-font uppercase">Rings Atelier</RouterLink>
    <nav class="nav-links">
      <a href="#studio" @click="scrollToSection">Студия</a>
      <a href="#masterclass" @click="scrollToSection">Мастер-классы</a>
      <RouterLink to="/catalog" class="nav-catalog">Каталог</RouterLink>
      <a href="#reviews" @click="scrollToSection">Отзывы</a>
    </nav>
    <a href="#contact" @click="scrollToSection" class="btn btn-primary header-cta" style="padding: 0.75rem 1.5rem; font-size: 0.75rem;">Записаться</a>

    <button
      type="button"
      class="mobile-menu-toggle"
      :class="{ open: isMenuOpen }"
      @click="toggleMenu"
      aria-label="Открыть меню"
      :aria-expanded="isMenuOpen"
    >
      <span></span>
      <span></span>
      <span></span>
    </button>
  </header>

  <Transition name="menu-fade">
    <div v-if="isMenuOpen" class="mobile-menu" @click.self="closeMenu">
      <nav class="mobile-nav">
        <a href="#studio" @click="scrollToSection">Студия</a>
        <a href="#masterclass" @click="scrollToSection">Мастер-классы</a>
        <RouterLink to="/catalog" @click="closeMenu">Каталог</RouterLink>
        <a href="#reviews" @click="scrollToSection">Отзывы</a>
        <a href="#contact" @click="scrollToSection" class="btn btn-primary mobile-cta">Записаться</a>
      </nav>
    </div>
  </Transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

watch(() => route.path, () => {
  isMenuOpen.value = false
})

const scrollToSection = async (e) => {
  closeMenu()
  const href = e.target.getAttribute('href')
  const sectionId = href.substring(1)

  if (router.currentRoute.value.path !== '/') {
    await router.push('/')
  }

  setTimeout(() => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }, 100)
}
</script>

<style scoped>
@keyframes glow-wave {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.nav-catalog {
  font-weight: 600;
  background: linear-gradient(
    90deg,
    var(--color-text) 0%,
    var(--color-text) 25%,
    var(--color-gold) 50%,
    var(--color-text) 75%,
    var(--color-text) 100%
  );
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: glow-wave 8s linear infinite;
}

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 40px;
  height: 40px;
  gap: 6px;
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 60;
}

@media (max-width: 1080px) {
  .mobile-menu-toggle {
    position: absolute;
    right: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
  }
}

.mobile-menu-toggle span {
  display: block;
  width: 24px;
  height: 2px;
  background: var(--color-text);
  transition: all 0.3s ease;
  transform-origin: center;
}

.mobile-menu-toggle.open span:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.mobile-menu-toggle.open span:nth-child(2) {
  opacity: 0;
}

.mobile-menu-toggle.open span:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}

.mobile-menu {
  position: fixed;
  inset: 0;
  background: rgba(2, 44, 34, 0.96);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  z-index: 55;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.75rem;
}

.mobile-nav a {
  font-size: 1.25rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 300;
  color: var(--color-text);
  transition: color 0.3s ease;
}

.mobile-nav a:hover {
  color: var(--color-gold);
}

.mobile-nav .nav-catalog {
  font-weight: 600;
}

.mobile-cta {
  margin-top: 1rem;
  padding: 0.875rem 2rem;
  font-size: 0.875rem;
}

.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: opacity 0.3s ease;
}

.menu-fade-enter-from,
.menu-fade-leave-to {
  opacity: 0;
}

@media (max-width: 1080px) {
  .mobile-menu-toggle {
    display: flex;
  }
}
</style>
