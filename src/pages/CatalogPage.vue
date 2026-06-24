<template>
  <div class="catalog-page">
    <Catalog />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useHead } from '@vueuse/head'
import Catalog from '../components/Catalog.vue'

useHead({
  title: 'Каталог | Обручальные и помолвочные кольца на заказ в Спб',
  meta: [
    {
      name: 'description',
      content: 'Каталог обручальных колец, помолвочных колец и украшений от Rings Atelier. Все модели можно изготовить на индивидуальном мастер-классе в Санкт-Петербурге.'
    },
    { property: 'og:title', content: 'Каталог | Обручальные и помолвочные кольца на заказ в Спб' },
    { property: 'og:description', content: 'Примеры обручальных и помолвочных колец, созданных на мастер-классах Rings Atelier в Санкт-Петербурге.' },
    { property: 'og:url', content: 'https://rings-atelier.ru/catalog' },
    { property: 'og:type', content: 'website' },
    { name: 'keywords', content: 'обручальные кольца на заказ спб, свадебные кольца, помолвочные кольца на заказ, помолвочное кольцо спб, составные кольца, кулон на заказ' }
  ],
  link: [
    { rel: 'canonical', href: 'https://rings-atelier.ru/catalog' }
  ]
})

onMounted(() => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.catalog-page {
  padding: 3rem 0;
}
</style>
