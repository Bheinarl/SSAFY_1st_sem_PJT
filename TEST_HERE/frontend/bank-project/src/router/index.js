import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import GamePage from '@/views/GamePage.vue';
import GameReal from '@/views/GameReal.vue';
import Finances from '@/views/Finances.vue';
import FinanceDeposit from '@/views/FinanceDeposit.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/profile', component: Profile },
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/exchange-rate-alert', component: ExchangeRateAlert },
    { path: '/game', component: GamePage },
    { path: '/gamereal', component: GameReal },
    { path: '/finances', component: Finances,
      children: [
        // { path: 'deposit', component: FinanceDeposit},
        // { path: '/finances', component: Finances},
        // { path: '/finances', component: Finances},
      ]
    }
  ]
})

export default router
