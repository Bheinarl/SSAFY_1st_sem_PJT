<template>
  <nav class="navbar">
    <!-- 왼쪽 메뉴 -->
    <div class="left-menu">
      <span v-show="isAuthenticated" @click="goFinances" class="nav-item">Finances</span>
      <span v-show="isAuthenticated">|</span>
      <span v-show="isAuthenticated" @click="goGame" class="nav-item">goGameReal</span>
      <span v-show="isAuthenticated">|</span>
      <span v-show="isAuthenticated" @click="goLeaderBoard" class="nav-item">LeaderBoard</span>
      <span v-show="isAuthenticated">|</span>
      <router-link v-show="isAuthenticated" to="/posts" class="nav-item">게시판</router-link>
    </div>

    <!-- 오른쪽 메뉴 -->
    <div class="right-menu">
      <router-link v-show="isAuthenticated" to="/profile" class="nav-item">Profile</router-link>
      <span v-show="isAuthenticated">|</span>
      <span v-show="isAuthenticated" @click="logout" class="nav-item">Logout</span>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(!!localStorage.getItem('token'));

const logout = () => {
  localStorage.removeItem('token');
  isAuthenticated.value = false;
  router.push('/login');
};

const goGame = () => {
  router.push('/gamereal');
};

const goFinances = () => {
  router.push('/finances');
};

const goLeaderBoard = () => {
  router.push('/leaderboard');
};

watch(() => router.currentRoute, () => {
  isAuthenticated.value = !!localStorage.getItem('token');
});
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  background-color: #feebd6; /* Navbar 배경색 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.left-menu,
.right-menu {
  display: flex;
  gap: 15px;
}

.nav-item {
  cursor: pointer;
  color: #000000; /* 기본 글자 색상 */
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: #ee6463; /* hover 시 강조 색상 */
}

span {
  color: #000000; /* 구분자 색상 */
}
</style>
