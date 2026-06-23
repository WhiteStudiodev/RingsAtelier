<template>
  <div class="legal-page">
    <div class="container">
      <div class="legal-header">
        <h1 class="legal-title heading-font">Политика конфиденциальности</h1>
        <div class="separator"></div>
        <p class="legal-subtitle">ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ СКВОРЦОВ АЛЕКСАНДР МИХАЙЛОВИЧ</p>
        <p class="legal-meta">г. Санкт-Петербург<br>13.01.2025</p>
      </div>
      <div class="legal-content">
        <section class="legal-section">
          <p>В Политике конфиденциальности (далее — Политика) указан перечень персональных данных (далее — Данные), которые могут быть запрошены у пользователей (далее — Пользователь) на сайте <a href="https://rings-atelier.ru">rings-atelier.ru</a> (далее — Сайт), а также способы обработки таких данных.</p>
          <p>Политика применяется также к информации, которую ИНДИВИДУАЛЬНЫЙ ПРЕДПРИНИМАТЕЛЬ СКВОРЦОВ АЛЕКСАНДР МИХАЙЛОВИЧ (далее — Оператор) получило в результате эксплуатации Пользователем его Сайта.</p>
        </section>

        <section class="legal-section">
          <h2>1. Предмет Политики</h2>
          <p><strong>1.1.</strong> Пользователь выражает и подтверждает свое согласие с Политикой, независимо от прохождения регистрации, при получении доступа или использовании каких-либо функций Сайта. Иначе Пользователь обязан прекратить использование Сайта.</p>
          <p><strong>1.2.</strong> Подлежащие обработке персональные данные Пользователя:</p>
          <ul>
            <li>фамилия, имя, отчество;</li>
            <li>контактный телефон;</li>
            <li>электронная почта.</li>
          </ul>
          <p><strong>1.3.</strong> Подлежащие обработке технические данные Пользователя:</p>
          <ul>
            <li>IP-адрес;</li>
            <li>данные браузера;</li>
            <li>время посещения Сайта;</li>
            <li>адрес страницы, на которой располагается рекламный блок;</li>
            <li>адрес предыдущей страницы.</li>
          </ul>
        </section>

        <section class="legal-section">
          <h2>2. Цели обработки Данных</h2>
          <p><strong>2.1.</strong> Оператор использует данные Пользователя для следующих целей:</p>
          <ul>
            <li>идентификация Пользователя для оформления заказа;</li>
            <li>создание личного кабинета;</li>
            <li>уведомления о статусе заказа;</li>
            <li>обработка и получение платежей;</li>
            <li>обратная связь с Пользователем, рассылки рекламно-информационных материалов;</li>
            <li>проведение маркетинговых, статистических и других исследований.</li>
          </ul>
        </section>

        <section class="legal-section">
          <h2>3. Способы и сроки обработки Данных</h2>
          <p><strong>3.1.</strong> Политика вступает в силу с момента, когда Пользователь в первый раз заходит на Сайт, и действует бессрочно.</p>
          <p><strong>3.2.</strong> Оператор может передавать Данные Пользователя курьерским и почтовым службам.</p>
        </section>

        <section class="legal-section">
          <h2>4. Защита Данных</h2>
          <p><strong>4.1.</strong> Оператор хранит и оберегает Данные от несанкционированного доступа и распространения в соответствии с внутренними правилами и регламентами.</p>
          <p><strong>4.2.</strong> Оператор сохраняет конфиденциальность в отношении Данных Пользователя за исключением случаев, когда Пользователь делает их общедоступными.</p>
        </section>

        <section class="legal-section">
          <h2>5. Права и обязанности</h2>
          <p><strong>5.1.</strong> Оператор охраняет конфиденциальность Данных Пользователя. Если Данные будут утрачены или разглашены, Оператор обязан уведомить об этом Пользователя.</p>
          <p><strong>5.2.</strong> Оператор обязан принять все меры, чтобы предотвратить убытки и другие негативные последствия утраты и разглашения Данных.</p>
          <p><strong>5.3.</strong> Оператор не вправе продавать, обменивать, публиковать или разглашать другими способами Данные Пользователя.</p>
          <p><strong>5.4.</strong> Оператор вправе изменять Политику. Пользователь обязан самостоятельно отслеживать изменения.</p>
          <p><strong>5.5.</strong> Пользователь вправе сделать запрос на блокировку Данных.</p>
        </section>

        <section class="legal-section">
          <h2>6. Разрешение споров</h2>
          <p><strong>6.1.</strong> Споры и разногласия Пользователя и Оператора по вопросам, связанным с Политикой, разрешаются на переговорах.</p>
          <p><strong>6.2.</strong> Если на переговорах Пользователь и Оператор не смогут достичь согласия, спор передается в суд.</p>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.legal-page {
  padding: 8rem 0 4rem;
  min-height: 100vh;
}

.legal-header {
  text-align: center;
  margin-bottom: 4rem;
}

.legal-title {
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 1.5rem;
  color: var(--color-gold);
}

.legal-subtitle {
  font-size: 1rem;
  color: var(--color-text);
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.legal-meta {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  line-height: 1.6;
}

.legal-content {
  max-width: 800px;
  margin: 0 auto;
}

.legal-section {
  margin-bottom: 2.5rem;
}

.legal-section h2 {
  font-family: var(--font-heading);
  font-size: 1.35rem;
  color: var(--color-text);
  margin-bottom: 1rem;
  margin-top: 2rem;
}

.legal-section p {
  color: var(--color-text-muted);
  line-height: 1.8;
  margin-bottom: 0.75rem;
}

.legal-section ul {
  list-style: none;
  padding: 0;
  color: var(--color-text-muted);
  line-height: 1.8;
  margin-bottom: 1rem;
}

.legal-section ul li {
  padding-left: 1.5rem;
  position: relative;
  margin-bottom: 0.5rem;
}

.legal-section ul li::before {
  content: '—';
  position: absolute;
  left: 0;
  color: var(--color-accent);
}

.legal-section a {
  color: var(--color-accent);
  transition: color 0.3s ease;
}

.legal-section a:hover {
  color: var(--color-gold);
}
</style>
