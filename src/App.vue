<template>
  <LoadingScreen />
  <div class="app-container">
    <BackgroundConstellation />

    <AppHeader />
    
    <main>
      <RouterView />
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import { useScrollReveal } from './composables/useScrollReveal'
import AppHeader from './components/AppHeader.vue'
import LoadingScreen from './components/LoadingScreen.vue'
import AppFooter from './components/AppFooter.vue'
import BackgroundConstellation from './components/BackgroundConstellation.vue'

useScrollReveal()
</script>

<style>
/* Global styles are in index.css */
</style>
