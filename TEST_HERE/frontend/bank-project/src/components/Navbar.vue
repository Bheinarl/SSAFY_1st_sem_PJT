<template>
  <nav class="navbar">
    <!-- 왼쪽 메뉴 -->
    <div class="left-menu">
      <span v-show="isAuthenticated" @click="goFinances" class="nav-item">금융상품</span>
      <span v-show="isAuthenticated">|</span>
      <span v-show="isAuthenticated" @click="goGame" class="nav-item">모의투자게임</span>
      <span v-show="isAuthenticated">|</span>
      <span v-show="isAuthenticated" @click="goLeaderBoard" class="nav-item">랭킹</span>
      <span v-show="isAuthenticated">|</span>
      <router-link v-show="isAuthenticated" to="/posts" class="nav-item">자유게시판</router-link>
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
    router.push('/');
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
  background-color: #1F509A; /* 메인 파란색 배경 */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.left-menu,
.right-menu {
  display: flex;
  gap: 15px;
}

.nav-item {
  cursor: pointer;
  color: #D4EBF8; /* 밝은 파란색 텍스트 */
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease;
}

.nav-item:hover {
  color: #E38E49; /* hover 시 따뜻한 주황색 */
}

span {
  color: #D4EBF8; /* 구분자 색상 */
}
</style>
