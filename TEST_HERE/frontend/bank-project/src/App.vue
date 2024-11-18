<script setup>
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';

// export default {
//   components: {
//     ExchangeRateAlert,
//     Navbar,
//   },
// };
// export default {
//   components: {
//     ExchangeRateAlert,
//   },
// };
// import CurrencyAlert from './components/CurrencyAlert.vue'
// import ExchangeRate from './components/ExchangeRate.vue'
</script>

<template>
  <header>
  </header>

  <main>
    <div id="app">
      <Navbar />
      <RouterView />
      <!-- <router-view /> -->

    </div>

    <section>
      <!-- 기존 CurrencyAlert와 ExchangeRate 대신 통합된 컴포넌트로 변경 -->
      <!-- <ExchangeRateAlert /> -->
    </section>

    <!-- CurrencyAlert 및 ExchangeRate 컴포넌트 추가
    <section>
      <h2>환율 알림 설정</h2>
      <CurrencyAlert />
      <h2>---------------</h2>
    </section>

    <section>
      <h2>현재 환율 정보</h2>
      <ExchangeRate />
    </section> -->
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
