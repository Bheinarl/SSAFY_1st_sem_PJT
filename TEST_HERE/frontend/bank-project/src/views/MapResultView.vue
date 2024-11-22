<template>
  <div class="map-container">
    <KakaoMap />
  </div>
</template>

<script>
import KakaoMap from '@/components/KakaoMap2.vue'

export default {
  name: 'MapResultView',
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