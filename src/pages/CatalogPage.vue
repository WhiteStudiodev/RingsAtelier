<template>
  <div class="catalog-page">
    <Catalog />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Catalog from '../components/Catalog.vue'

onMounted(() => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.catalog-page {
  padding: 3rem 0;
}
</style>
