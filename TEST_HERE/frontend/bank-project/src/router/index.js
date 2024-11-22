import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import GameReal from '@/views/GameReal.vue';
import MapView from '@/views/MapView.vue'  // 추가

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/profile', component: Profile },
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/exchange-rate-alert', component: ExchangeRateAlert },
    // { path: '/map', component: MapView },
    { path: '/gamereal', component: GameReal },
    { path: '/mapview', component: MapView },  // 추가

  ],
})

export default router
