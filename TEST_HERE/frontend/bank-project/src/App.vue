<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, computed } from 'vue';
import { RouterView } from 'vue-router';

// 토큰 존재 여부를 계산
const showNavbar = computed(() => !!localStorage.getItem('token')); 
console.log(showNavbar.value)
</script>

<template>
  <main>
    <RouterView />
  </main>
</template>

<style scoped>
main {
  padding: 0;
}
</style>