import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './pages/HomePage.vue'

const CatalogPage = () => import('./pages/CatalogPage.vue')
const PrivacyPolicy = () => import('./pages/PrivacyPolicy.vue')
const PersonalDataPolicy = () => import('./pages/PersonalDataPolicy.vue')
const PublicOffer = () => import('./pages/PublicOffer.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/catalog',
    name: 'Catalog',
    component: CatalogPage
  },
  {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy
  },
  {
    path: '/personal-data',
    name: 'PersonalDataPolicy',
    component: PersonalDataPolicy
  },
  {
    path: '/offer',
    name: 'PublicOffer',
    component: PublicOffer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
