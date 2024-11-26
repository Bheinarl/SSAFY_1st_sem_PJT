<template>
  <main class="app-main">
    <RouterView />
  </main>
</template>

<script setup>
import { computed } from 'vue';

// 토큰 존재 여부 계산
const showNavbar = computed(() => !!localStorage.getItem('token'));
console.log(showNavbar.value);
</script>

<style scoped>
.app-main {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 전체를 채우도록 설정 */
  background-color: #1F509A; /* home.vue와 일치 */
  position: relative; /* 자식 요소의 위치 제어 */
  overflow: hidden; /* 불필요한 스크롤 방지 */
}
</style>
