import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import GamePage from '@/views/GamePage.vue';
import StockChart from "../components/StockChart.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/profile', component: Profile },
    { path: '/register', component: Register },
    { path: '/login', component: Login },
    { path: '/exchange-rate-alert', component: ExchangeRateAlert },
    { path: '/game', component: GamePage },
    {
      path: "/stocks", // /stocks 경로에서 StockChart 컴포넌트 출력
      name: "Stocks",
      component: StockChart,
    },
  ],
})

export default router
