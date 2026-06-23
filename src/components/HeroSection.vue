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
        <h1 class="hero-title heading-font">Создайте своё <br><i class="text-gradient">наследие</i></h1>
        <p class="hero-desc body-font font-light">Доверьтесь процессу. В нашей премиальной студии вы пройдете весь путь от расплавленного металла до уникального ювелирного кольца.</p>
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
