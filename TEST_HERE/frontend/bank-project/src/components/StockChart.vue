<template>
  <div>
    <h1>Stock Investment Game</h1>
    <select v-model="selectedStock" @change="fetchStockData">
      <option value="005930">Samsung Electronics</option>
      <option value="000660">SK Hynix</option>
      <option value="035420">Naver</option>
    </select>
    <ChartComponent :stockData="stockData" :currentDay="currentDay" />
    <button @click="nextDay">Next Day</button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import ChartComponent from './ChartComponent.vue';
import axios from 'axios';

const selectedStock = ref("005930");
const stockData = ref([]);
const currentDay = ref(1);

const fetchStockData = async () => {
  try {
    console.log('Fetching stock data for:', selectedStock.value);
    const response = await axios.get(`/api/stocks/${selectedStock.value}/`, {
      params: {
        start: '2024-07-01',
        end: '2024-07-10'
      }
    });
    if (response.data.status === 'success') {
      stockData.value = response.data.data;
      console.log('Stock data fetched:', stockData.value);
    } else {
      console.error('Error:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error.response ? error.response.data : error.message);
  }
};

const nextDay = () => {
  if (currentDay.value < 10) {
    currentDay.value++;
  } else {
    alert('Game over');
  }
};

watch(selectedStock, fetchStockData);

fetchStockData(); // 초기 데이터 로드
</script>

<style scoped>
/* 스타일 정의 */
</style>
