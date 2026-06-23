<template>
  <section class="reviews-section" id="reviews">
    <div class="container">
      <div class="section-header" data-reveal>
        <span class="section-subtitle uppercase tracking-widest">Социальное доказательство</span>
        <h2 class="section-title heading-font">Что говорят о нас</h2>
        <div class="separator"></div>
      </div>

      <div class="reviews-layout">
        <!-- Rating Highlight -->
        <div class="rating-block glass-card" data-reveal>
          <div class="rating-stars">
            <svg v-for="i in 5" :key="i" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2l2.9 6.9L22 10l-5.5 4.8L18 22l-6-3.5L6 22l1.5-7.2L2 10l7.1-1.1L12 2z"/>
            </svg>
          </div>
          <div class="rating-value heading-font">
            <span class="rating-number text-gradient">5.0</span>
            <span class="rating-max">/ 5.0</span>
          </div>
          <p class="rating-source">на Яндекс Картах</p>
          <div class="rating-divider"></div>
          <p class="rating-text font-light">
            Высокий рейтинг — результат нашей любви к делу и каждому гостю.
            Ваше доверие вдохновляет на создание шедевров.
          </p>
          <a
            href="https://yandex.com/maps/org/rings_atelier/243740413465/reviews"
            target="_blank"
            rel="noopener"
            class="rating-button"
          >
            <span>Смотреть все отзывы</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M7 17l9.2-9.2M8 7h9v9"/>
            </svg>
          </a>
        </div>

        <!-- Testimonial Cards -->
        <div class="reviews-list">
          <article
            v-for="(review, index) in reviews"
            :key="index"
            class="review-card glass-card"
            data-reveal
            :data-reveal-delay="index + 1"
          >
            <div class="review-quote-mark heading-font">"</div>
            <p class="review-text font-light">{{ review.text }}</p>
            <div class="review-footer">
              <div class="review-author">
                <div class="review-name heading-font">{{ review.name }}</div>
                <div class="review-date">{{ review.date }}</div>
              </div>
              <div class="review-stars">
                <svg v-for="i in 5" :key="i" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2l2.9 6.9L22 10l-5.5 4.8L18 22l-6-3.5L6 22l1.5-7.2L2 10l7.1-1.1L12 2z"/>
                </svg>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const reviews = [
  {
    name: 'Яна Ш',
    date: '31 мая 2026',
    text: 'Заказывали обручальные кольца в Rings Atelier — и это было лучшим решением! Кольца были изготовлены очень быстро, точно по эскизу, получились именно такими, как мы хотели.\n\nТакже хочется отметить классный сервис: вежливое общение, быстрые ответы в соцсетях, подарок в виде фото на полароид, красивейшую упаковку и дальнейшее обслуживание колечек.\n\nОстались очень довольны, спасибо Rings Atelier за эти эмоции в такой трепетный для нас момент!'
  },
  {
    name: 'Юлия К',
    date: '26 мая 2026',
    text: 'Рассматривала все студии города, представляющие МК по изготовлению обручальных колец, но именно Rings Atelier с первого касания влюбили в себя! Спасибо за безупречный сервис и трепетное отношение к своим клиентам, чувствуется, что здесь вас действительно слышат и стараются помочь в решении любого вопроса. Ребята прям на примерке постарались воссоздать желаемую нами фактуру, которой изначально не было в ассортименте, так мы смогли воплотить в жизнь свои фантазии прям на МК, создавая колечки своими руками от начала и до конца! Процесс невероятно интересный и символичный, особое чувство носить кольца, которые вы с такой любовью делали друг для друга. А приятные дополнения в виде ароматного кофе, смонтированного видео, первого фото на полароид и потрясающей комплектации при вручении готовых колечек, просто не оставляют равнодушным и дарят понимание, что ты выбрал лучшую студию из всех возможных и теперь это одно большое прекрасное воспоминание, которое останется внутри нас и на безымянных пальцах! 🦢✨'
  },
  {
    name: 'Максим С',
    date: '4 мая 2026',
    text: 'Воплотили идеи в золото и с бриллиантами!\n\nИскали с Ксенией что-то особенное для свадьбы, так как обычные кольца из ювелирных сетей нам не подходили. Хотелось уникальный дизайн и качественное исполнение — в этом ателье наши запросы реализовали на все сто.\n\nОписали свои идеи и получили уникальный собственный дизайн. Отдельно порадовала возможность компенсировать стоимость материала своим золотом: у нас было золотое украшение, которое просто лежало без дела, а здесь оно пошло в зачёт заказа. Это позволило получить кольца мечты на очень выгодных условиях, не переплачивая за металл.\n\nМы ещё не расписались, подготовка в самом разгаре, но один из самых важных вопросов уже закрыт. Огромное спасибо мастерам за работу и за то, что пошли навстречу в вопросе материалов.\n\nМаксим и Ксения.'
  }
]
</script>

<style scoped>
.reviews-section {
  padding: 5rem 0;
}

.reviews-layout {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 2.5rem;
  margin-top: 3rem;
  align-items: start;
}

/* Rating Block */
.rating-block {
  padding: 3rem 2.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  position: sticky;
  top: 6rem;
}

.rating-stars {
  display: flex;
  gap: 0.35rem;
  color: var(--color-gold);
}

.rating-stars svg {
  width: 22px;
  height: 22px;
}

.rating-value {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.rating-number {
  font-size: 4.5rem;
  line-height: 1;
}

.rating-max {
  font-size: 1.25rem;
  color: var(--color-text-muted);
}

.rating-source {
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--color-text-muted);
}

.rating-divider {
  width: 40px;
  height: 1px;
  background: var(--color-gold);
  opacity: 0.5;
  margin: 0.75rem 0;
}

.rating-text {
  font-size: 0.95rem;
  color: var(--color-text-muted);
  line-height: 1.7;
  max-width: 280px;
}

.rating-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-gold);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  font-weight: 600;
  padding-bottom: 4px;
  border-bottom: 1px solid rgba(212, 165, 116, 0.3);
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.rating-button:hover {
  color: var(--color-text);
  border-color: var(--color-gold);
  transform: translateY(-2px);
}

/* Review Cards */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.review-card {
  padding: 2rem 2.25rem;
  position: relative;
  border: 1px solid rgba(255, 255, 255, 0.05);
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.review-card:hover {
  border-color: rgba(212, 165, 116, 0.3);
  transform: translateY(-3px);
}

.review-quote-mark {
  position: absolute;
  top: 0.5rem;
  left: 1.5rem;
  font-size: 4rem;
  line-height: 1;
  color: var(--color-gold);
  opacity: 0.25;
  pointer-events: none;
}

.review-text {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--color-text);
  margin: 0 0 1.5rem;
  position: relative;
  z-index: 1;
  white-space: pre-line;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.review-name {
  font-size: 1.05rem;
  color: var(--color-text);
}

.review-date {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin-top: 0.15rem;
}

.review-stars {
  display: flex;
  gap: 0.2rem;
  color: var(--color-gold);
}

.review-stars svg {
  width: 14px;
  height: 14px;
}

@media (max-width: 1024px) {
  .reviews-layout {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
  .rating-block {
    position: static;
    max-width: 480px;
    margin: 0 auto;
  }
}
</style>
