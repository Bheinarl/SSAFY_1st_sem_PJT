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
          <div class="balance-info">Cash: $<span>{{ cash.toFixed(2) }}</span></div>
          <div class="balance-info">Portfolio Value: $<span>{{ portfolioValue.toFixed(2) }}</span></div>
          <div class="balance-info">Total Value: $<span>{{ totalValue.toFixed(2) }}</span></div>
        </div>

        <div class="chart-section">
          <canvas id="chart"></canvas>
        </div>

        <div class="trading-panel">
          <select v-model="selectedStock" @change="updateChart">
            <option value="AAPL">Apple (AAPL)</option>
            <option value="MSFT">Microsoft (MSFT)</option>
            <option value="GOOGL">Google (GOOGL)</option>
          </select>

          <div class="stock-info">
            <h3>Current Price: $<span>{{ currentPrice.toFixed(2) }}</span></h3>
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
import axios from 'axios';
import Chart from 'chart.js/auto';

const currentDay = ref(1);
const cash = ref(100000);
const portfolio = ref({});
const selectedStock = ref('AAPL');
const tradeVolume = ref(0);
const stockData = ref({});
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

function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`),
      datasets: [{
        label: 'Stock Price',
        data: stockData.value[selectedStock.value] || [],
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
    chart.data.datasets[0].data = stockData.value[selectedStock.value];
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
    alert('Game over');
  }
}

onMounted(async () => {
  try {
    const response = await axios.get('/stocks/api/stock-data/');
    stockData.value = response.data;
    initializeChart();
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
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