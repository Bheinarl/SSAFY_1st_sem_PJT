<template>
  <div>
    <div class="header">
      <div class="container">
        <h1>10-Day Stock Investment Game</h1>
      </div>
    </div>

    <div class="container">
      <div class="day-counter">Day <span>{{ currentDay }}</span> / 10</div>
      
      <div class="game-container">
        <div class="balance-panel">
          <h3>Account Balance</h3>
          <div class="balance-info">Cash: ₩<span>{{ cash.toFixed(2) }}</span></div>
          <div class="balance-info">Portfolio Value: ₩<span>{{ portfolioValue.toFixed(2) }}</span></div>
          <div class="balance-info">Total Value: ₩<span>{{ totalValue.toFixed(2) }}</span></div>
        </div>

        <div class="chart-section">
          <canvas id="chart"></canvas>
        </div>

        <div class="trading-panel">
          <select v-model="selectedStock" @change="updateStockUrl">
            <option value="삼성전자">삼성전자</option>
            <option value="SK하이닉스">SK하이닉스</option>
            <option value="현대차">현대차</option>
            <option value="POSCO홀딩스">POSCO홀딩스</option>
            <option value="두산에너빌리티">두산에너빌리티</option>
            <option value="셀트리온">셀트리온</option>
            <option value="NAVER">NAVER</option>
            <option value="기아">기아</option>
            <option value="LG에너지솔루션">LG에너지솔루션</option>
            <option value="롯데케미칼">롯데케미칼</option>
          </select>

          <div class="stock-info">
            <h3>Current Price: ₩<span>{{ currentPrice.toFixed(2) }}</span></h3>
          </div>

          <input type="number" v-model.number="tradeVolume" placeholder="Enter quantity">

          <div class="trade-buttons">
            <button @click="executeTrade('buy')">Buy</button>
            <button @click="executeTrade('sell')">Sell</button>
          </div>
        </div>

        <div class="portfolio">
          <h3>Your Holdings</h3>
          <div>
            <div v-for="(quantity, stock) in portfolio" :key="stock">
              {{ stock }}: {{ quantity }} shares
            </div>
          </div>
        </div>

        <button @click="nextDay">Next Day</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import axios from 'axios';
import Chart from 'chart.js/auto';
import api from '@/api';

const stockStore = useStockStore();

const currentDay = ref(1);
const cash = ref(10000000);
const portfolio = ref({});
const selectedStock = ref('삼성전자');
const tradeVolume = ref(0);
const stockData = ref({
  '삼성전자': [],
  'SK하이닉스': [],
  '현대차': [],
  'POSCO홀딩스': [],
  '두산에너빌리티': [],
  '셀트리온': [],
  'NAVER': [],
  '기아': [],
  'LG에너지솔루션': [],
  '롯데케미칼': [],
});
let chart;

const portfolioValue = computed(() => {
  return Object.keys(portfolio.value).reduce((total, stock) => {
    return total + (portfolio.value[stock] * (stockData.value[stock]?.[currentDay.value - 1] || 0));
  }, 0);
});

const totalValue = computed(() => {
  return cash.value + portfolioValue.value;
});

const currentPrice = computed(() => {
  return stockData.value[selectedStock.value]?.[currentDay.value - 1] || 0;
});

function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];
  if (stockCode) {
    const apiUrl = `http://127.0.0.1:8000/api/stocks/${stockCode}/`;
    console.log('API URL:', apiUrl);
    fetchStockData(apiUrl);
  }
}

async function fetchStockData(apiUrl) {
  try {
    const response = await axios.get(apiUrl);
    console.log('API Response:', response); // 응답 데이터 확인
    if (response.data.status === 'success') {
      stockData.value[selectedStock.value] = response.data.data.map(item => item.open_price);
      updateChart();
    } else {
      console.error('Error fetching stock data:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
}

function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`),
      datasets: [{
        label: 'Stock Price',
        data: stockData.value[selectedStock.value].slice(0, currentDay.value),
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false  
        }
      }
    }
  });
}

function updateChart() {
  if (chart && stockData.value[selectedStock.value]) {
    chart.data.datasets[0].data = stockData.value[selectedStock.value].slice(0, currentDay.value);
    chart.update();
  }
}

function executeTrade(type) {
  const volume = tradeVolume.value;
  const price = currentPrice.value;
  if (type === 'buy') {
    if (cash.value >= price * volume) {
      cash.value -= price * volume;
      portfolio.value[selectedStock.value] = (portfolio.value[selectedStock.value] || 0) + volume;
    } else {
      alert('Not enough cash');
    }
  } else if (type === 'sell') {
    if ((portfolio.value[selectedStock.value] || 0) >= volume) {
      cash.value += price * volume; // cash should increase when selling
      portfolio.value[selectedStock.value] -= volume;
    } else {
      alert('Not enough shares');
    }
  }
}

function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;
    updateChart();
  } else {
    console.log(totalValue.value);
    alert(`Game over. Your total value is ₩${totalValue.value}`);
  }
}

onMounted(() => {
  updateStockUrl();
  initializeChart();
});

// Watchers to update the UI when values change
watch([cash, portfolio, currentDay, selectedStock], () => {
  updateChart();
});
</script>

<style scoped>
.chart-section {
  width: 80%; /* Adjust the width as needed */
  height: 300px; /* Adjust the height as needed */
  margin: 0 auto; /* Center the chart */
}
</style>