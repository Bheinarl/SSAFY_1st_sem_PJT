<template>
  <div class="map-container">
    <KakaoMap />
  </div>
</template>

<script>
import KakaoMap from '@/components/KakaoMap.vue'

export default {
  components: {
    KakaoMap
  }
}
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100vh;
}
</style>