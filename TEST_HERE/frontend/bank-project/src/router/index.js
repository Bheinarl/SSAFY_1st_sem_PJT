import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue';
import Profile from '@/views/Profile.vue';
import Register from '@/views/Register.vue';
import Login from '@/views/Login.vue';
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import GameReal from '@/views/GameReal.vue';
import Finances from '@/components/Finances.vue';
import MapView from '@/views/MapView.vue';

import Board from '@/views/Board.vue';
import PostDetail from '@/views/PostDetail.vue';
import PostCreate from '@/views/PostCreate.vue'; // 글 작성 페이지 추가
import PostEdit from '@/views/PostEdit.vue'; // 글 수정 페이지 추가
import LeaderBoard from '@/components/LeaderBoard.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: Home },
    { path: '/profile', component: Profile },
    
    { path: '/posts', component: Board, name: 'Board' },  // 게시판 목록
    { path: '/posts/new', component: PostCreate, name: 'PostCreate' },  // 글 작성
    { path: '/posts/:id', component: PostDetail, name: 'PostDetail' },  // 게시글 상세
    { path: '/posts/:id/edit', component: PostEdit, name: 'PostEdit' },  // 게시글 수정

    { path: '/register', component: Register, },
    { path: '/login', component: Login },
    { path: '/exchange-rate-alert', component: ExchangeRateAlert },
    { path: '/gamereal', component: GameReal },
    { path: '/mapview', component: MapView },
    { path: '/finances', component: Finances },
    { path: '/leaderboard', component: LeaderBoard },
  ]
})

export default router
