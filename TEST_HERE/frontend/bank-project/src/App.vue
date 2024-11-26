<script setup>
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <header>
    <Navbar />
  </header>
  <body>
    <main>
      <RouterView />
    </main>
  </body>
</template>

<style scoped>
/* 기본 배경색 설정 */
body {
  margin: 0;
  padding: 0;
  background-color: #1F509A;; /* 페이지 배경 */
  font-family: Arial, sans-serif;
}

header {
  background-color: #feebd6; /* Navbar 배경색 */
}

/* main의 여백 제거 */
main {
  padding: 20px;
  min-height: calc(100vh - 60px); /* 전체 화면 높이에서 Navbar 제외 */
}
</style>