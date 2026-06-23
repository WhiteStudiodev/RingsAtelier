<template>
  <section class="gifts-section" id="gifts">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Приятные бонусы</span>
        <h2 class="section-title heading-font">Что входит в мастер-класс</h2>
        <div class="separator"></div>
      </div>

      <div class="gifts-grid">
        <div
          v-for="(gift, index) in gifts"
          :key="index"
          class="gift-item"
          data-reveal
          :data-reveal-delay="index"
        >
          <div class="gift-num heading-font">{{ String(index + 1).padStart(2, '0') }}</div>
          <div class="gift-icon-wrap">
            <div class="gift-icon" v-html="gift.icon"></div>
          </div>
          <h3 class="gift-title heading-font">{{ gift.title }}</h3>
          <p class="gift-desc font-light">{{ gift.desc }}</p>
        </div>
      </div>

      <p class="gifts-footnote font-light" data-reveal>
        Все бонусы — без доплат, входят в стоимость мастер-класса
      </p>
    </div>
  </section>
</template>

<script setup>
const gifts = [
  {
    title: 'Эксклюзивная гравировка',
    desc: 'Любая надпись, дата или символ внутри кольца — навсегда с вами.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21l4-1 12-12-3-3-12 12-1 4z"/><path d="M15 6l3 3"/><path d="M14 17h7"/></svg>`
  },
  {
    title: 'Видеосъёмка процесса',
    desc: 'Профессиональное видео того, как рождаются ваши кольца.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="14" height="10" rx="1"/><path d="M16 10l6-3v10l-6-3z"/></svg>`
  },
  {
    title: 'Рилс на память',
    desc: 'Готовый ролик в формате reels — собранный нашим монтажёром.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M3 9h18"/><path d="M8 3l3 6"/><path d="M14 3l3 6"/><path d="M10 13l5 3-5 3z" fill="currentColor"/></svg>`
  },
  {
    title: 'Полароид на память',
    desc: 'Мгновенный снимок, который вы заберёте с собой в этот же день.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="1"/><rect x="6" y="5" width="12" height="11"/><path d="M9 19h6"/></svg>`
  },
  {
    title: 'Ужин у партнёров',
    desc: 'Депозит в один из ресторанов-партнёров — для романтического вечера.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3v8a2 2 0 0 0 2 2v8"/><path d="M11 3v6a2 2 0 0 1-4 0V3"/><path d="M17 21V3c-1.5 0-3 1.5-3 5s1.5 5 3 5"/></svg>`
  },
  {
    title: 'Парковка за наш счёт',
    desc: 'Оплачиваем парковку всё время вашего мастер-класса.',
    icon: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 17V7h4.5a3 3 0 1 1 0 6H9"/></svg>`
  }
]
</script>

<style scoped>
.gifts-section {
  padding: 5rem 0;
}

.gifts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: rgba(212, 165, 116, 0.12);
  border: 1px solid rgba(212, 165, 116, 0.12);
  margin-top: 3rem;
}

.gift-item {
  background: var(--color-bg);
  padding: 2.5rem 2rem;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition:
    background 0.4s ease,
    transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 0.4s ease;
}

.gift-item:hover {
  background: rgba(212, 165, 116, 0.04);
  transform: translateY(-4px);
  box-shadow: 0 12px 30px -10px rgba(0, 0, 0, 0.5);
  z-index: 1;
}

.gift-num {
  position: absolute;
  top: 1.25rem;
  right: 1.5rem;
  font-size: 0.85rem;
  letter-spacing: 0.15em;
  color: var(--color-gold);
  opacity: 0.6;
}

/* Icon in gold circle outline */
.gift-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 1px solid rgba(212, 165, 116, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  transition: border-color 0.4s ease, transform 0.4s ease, background 0.4s ease;
  position: relative;
}

.gift-icon-wrap::before {
  content: '';
  position: absolute;
  inset: 4px;
  border-radius: 50%;
  border: 1px solid rgba(212, 165, 116, 0.1);
  transition: border-color 0.4s ease;
}

.gift-item:hover .gift-icon-wrap {
  border-color: rgba(212, 165, 116, 0.8);
  background: rgba(212, 165, 116, 0.05);
  transform: scale(1.05);
}

.gift-item:hover .gift-icon-wrap::before {
  border-color: rgba(212, 165, 116, 0.3);
}

.gift-icon {
  color: var(--color-gold);
  width: 28px;
  height: 28px;
  transition: transform 0.4s ease;
  position: relative;
  z-index: 1;
}

.gift-icon :deep(svg) {
  width: 100%;
  height: 100%;
}

.gift-item:hover .gift-icon {
  transform: scale(1.1);
}

.gift-title {
  font-size: 1.25rem;
  color: var(--color-text);
  margin: 0;
}

.gift-desc {
  font-size: 0.92rem;
  color: var(--color-text-muted);
  line-height: 1.6;
  margin: 0;
}

.gifts-footnote {
  margin-top: 2.5rem;
  text-align: center;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  letter-spacing: 0.02em;
  font-style: italic;
  position: relative;
}

.gifts-footnote::before,
.gifts-footnote::after {
  content: '';
  display: inline-block;
  width: 24px;
  height: 1px;
  background: rgba(212, 165, 116, 0.4);
  vertical-align: middle;
  margin: 0 1rem;
}

@media (max-width: 900px) {
  .gifts-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .gifts-grid {
    grid-template-columns: 1fr;
  }
  .gift-item {
    padding: 2rem 1.5rem;
  }
}
</style>
