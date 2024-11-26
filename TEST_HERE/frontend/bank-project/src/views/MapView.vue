<template>
  <header> <Navbar /> </header>
  <div class="map-container">
    <KakaoMap />
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
import KakaoMap from '@/components/KakaoMap.vue';
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}
</style>