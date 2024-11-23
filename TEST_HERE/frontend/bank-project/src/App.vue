<script setup>
import ExchangeRateAlert from '@/components/ExchangeRateAlert.vue';
import { onMounted } from 'vue';
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
import { RouterView } from 'vue-router';
import { useStockStore } from './stores/StockStore';

const stockStore = useStockStore();

const tickers = stockStore.tickers;

async function updateStockUrl() {
    const apiUrl = 'http://127.0.0.1:8000/stocks/api/stocks/list/';
    console.log('API URL:', apiUrl);
    try {
        const response = await axios.get(apiUrl);
    } catch (error) {
        console.error('Error fetching stock data:', error);
    }
}


onMounted(() => {
  updateStockUrl(); // await 키워드를 사용하여 비동기 호출
});

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
    </section>
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
