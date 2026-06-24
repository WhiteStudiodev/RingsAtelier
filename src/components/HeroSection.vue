<template>
  <section class="hero" id="studio">
    <div class="hero-video-container">
      <video autoplay muted loop playsinline preload="none" :poster="posterSrc">
        <source :src="videoSrc" type="video/webm">
      </video>
      <div class="hero-video-overlay"></div>
    </div>
    <div class="container hero-grid">
      <div class="hero-content" data-reveal>
        <span class="subtitle uppercase tracking-widest">✦ Ювелирное мастерство</span>
        <h1 class="hero-title heading-font">
          Создайте обручальные <br>
          <i class="text-gradient">кольца своими руками</i>
          <span class="hero-title-add">на мастер-классе или оформите индивидуальное изготовление колец на заказ</span>
        </h1>
        <p class="hero-desc body-font font-light">Ювелирный мастер-класс в Санкт-Петербурге для тех, кто хочет создать уникальные обручальные или помолвочные кольца из золота, серебра или платины.</p>
        <div class="hero-actions">
          <a href="#contact" class="btn btn-primary">Записаться на мастер-класс</a>
          <a href="#masterclass" class="btn btn-secondary">Узнать больше</a>
        </div>
      </div>
      
      <div class="hero-image-wrapper" data-reveal data-reveal-delay="1">
        <div class="glass-card hero-image-card animate-levitate">
          <img :src="heroImage" alt="Процесс создания кольца" width="814" height="1280" loading="eager" decoding="async">
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import videoSrc from '../assets/Hero_Video.webm'
import heroImage from '../assets/Glavn.webp'
import posterSrc from '../assets/hero-poster.webp'
</script>

<style scoped>
.hero-title-add {
  display: block;
  font-size: clamp(1rem, 1.8vw, 1.35rem);
  font-weight: 300;
  font-style: normal;
  margin-top: 1rem;
  color: var(--color-text);
  line-height: 1.4;
  letter-spacing: 0.02em;
}

@media (max-width: 768px) {
  .hero-title-add {
    margin-top: 0.75rem;
    font-size: 0.95rem;
  }
}
</style>
