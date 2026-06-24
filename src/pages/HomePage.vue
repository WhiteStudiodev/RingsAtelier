<template>
  <HeroSection />
  <Masterclasses />
  <div class="section-divider">✦</div>
  <ClientsCarousel />
  <div class="section-divider">✦</div>
  <Gifts />
  <div class="section-divider">✦</div>
  <Reviews />
  <div class="section-divider">✦</div>
  <Contacts />

  <!-- SEO-текст: виден пользователю, но оформлен аккуратно -->
  <section class="seo-text" aria-label="О студии">
    <div class="container">
      <div class="seo-content">
        <p>
          <strong>Rings Atelier</strong> — ювелирная мастерская в центре Санкт-Петербурга, где вы можете
          <strong>создать обручальные кольца своими руками</strong>. Мы проводим премиальные
          <strong>ювелирные мастер-классы в Спб</strong> для пар, семей и тех, кто ищет необычное
          <strong>романтическое свидание</strong>.
        </p>
        <p>
          На нашем <strong>парном мастер-классе</strong> вы пройдёте весь путь — от плавки металла до финальной полировки —
          и заберёте домой уникальные <strong>обручальные кольца на заказ</strong>. Доступны золото 585 и 750 пробы,
          серебро 925, платина, бриллианты и индивидуальная гравировка. Также у нас можно изготовить
          <strong>помолвочное кольцо</strong>, <strong>кулон на заказ</strong> или
          <strong>свадебные кольца на мастер-классе</strong>.
        </p>
        <p>
          Запишитесь на <strong>индивидуальный мастер-класс</strong>,
          <strong>семейный мастер-класс</strong> или <strong>мастер-класс для родителей</strong>.
          Это прекрасный <strong>подарок невесте</strong>, <strong>подарок жениху</strong> или совместный опыт,
          который останется с вами на всю жизнь.
        </p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useHead } from '@vueuse/head'
import HeroSection from '../components/HeroSection.vue'
import ClientsCarousel from '../components/ClientsCarousel.vue'
import Masterclasses from '../components/Masterclasses.vue'
import Gifts from '../components/Gifts.vue'
import Reviews from '../components/Reviews.vue'
import Contacts from '../components/Contacts.vue'

useHead({
  title: 'Rings Atelier | Обручальные кольца своими руками в Спб',
  meta: [
    {
      name: 'description',
      content: 'Ювелирный мастер-класс в Санкт-Петербурге. Создайте обручальные кольца своими руками из золота, серебра или платины. Парный, семейный и индивидуальный мастер-класс. Запись на Мясной, 20.'
    },
    { property: 'og:title', content: 'Rings Atelier | Обручальные кольца своими руками в Спб' },
    { property: 'og:description', content: 'Премиальный ювелирный мастер-класс в центре Санкт-Петербурга. Создайте обручальные кольца своими руками — от плавки металла до готового украшения.' },
    { property: 'og:url', content: 'https://rings-atelier.ru/' },
    { property: 'og:type', content: 'website' },
    { name: 'keywords', content: 'обручальные кольца спб, обручальные кольца на заказ, обручальные кольца своими руками, ювелирный мастер-класс спб, парный мастер класс, семейный мастер класс, романтическое свидание, помолвочное кольцо спб, кольца своими руками спб' }
  ],
  link: [
    { rel: 'canonical', href: 'https://rings-atelier.ru/' }
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@graph': [
          {
            '@type': 'Organization',
            '@id': 'https://rings-atelier.ru/#organization',
            name: 'Rings Atelier',
            url: 'https://rings-atelier.ru',
            logo: 'https://rings-atelier.ru/favicon.svg',
            description: 'Ювелирная мастерская и мастер-классы по созданию обручальных колец в Санкт-Петербурге.',
            sameAs: [
              'https://t.me/RingsAtelier',
              'https://vk.ru/rings.atelier'
            ],
            contactPoint: {
              '@type': 'ContactPoint',
              telephone: '+7-999-068-78-07',
              contactType: 'sales',
              areaServed: 'RU',
              availableLanguage: 'Russian'
            }
          },
          {
            '@type': 'LocalBusiness',
            '@id': 'https://rings-atelier.ru/#localbusiness',
            name: 'Rings Atelier',
            image: 'https://rings-atelier.ru/favicon.svg',
            url: 'https://rings-atelier.ru',
            telephone: '+7 (999) 068‑78‑07',
            email: 'info@rings-atelier.ru',
            address: {
              '@type': 'PostalAddress',
              streetAddress: 'улица Мясная, 20',
              addressLocality: 'Санкт-Петербург',
              addressCountry: 'RU'
            },
            geo: {
              '@type': 'GeoCoordinates',
              latitude: '59.9276',
              longitude: '30.3493'
            },
            openingHoursSpecification: {
              '@type': 'OpeningHoursSpecification',
              dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
              opens: '10:00',
              closes: '21:00'
            },
            priceRange: '$$$$',
            aggregateRating: {
              '@type': 'AggregateRating',
              ratingValue: '5.0',
              reviewCount: '50'
            }
          },
          {
            '@type': 'Service',
            name: 'Ювелирный мастер-класс по созданию обручальных колец',
            provider: { '@id': 'https://rings-atelier.ru/#localbusiness' },
            areaServed: {
              '@type': 'City',
              name: 'Санкт-Петербург'
            },
            description: 'Парный, семейный и индивидуальный мастер-класс по созданию обручальных колец, помолвочных колец и украшений из золота, серебра и платины.'
          }
        ]
      })
    }
  ]
})
</script>

<style scoped>
.seo-text {
  padding: 4rem 0 5rem;
  background: linear-gradient(180deg, rgba(2, 44, 34, 0) 0%, rgba(2, 44, 34, 0.6) 100%);
}

.seo-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  line-height: 1.8;
}

.seo-content p {
  margin-bottom: 1rem;
}

.seo-content strong {
  color: var(--color-text);
  font-weight: 500;
}

@media (max-width: 640px) {
  .seo-content {
    font-size: 0.85rem;
    line-height: 1.7;
  }
}
</style>
