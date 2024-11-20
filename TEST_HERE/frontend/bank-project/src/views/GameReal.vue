<template>
  <div>
    <!-- Header Section -->
    <div class="header">
      <div class="container">
        <h1>10-Day Stock Investment Game</h1>
      </div>
    </div>

    <!-- News Section -->
    <div class="news-container">
      <h3>Latest News</h3>
      <h3>{{ formattedDate }}</h3> <!-- 디버깅용으로 날짜 출력. 추후 삭제 -->
      <ul> <!-- 있는 뉴스 다 출력, 최대 10개까지만-->
        <li v-for="(title, index) in newsTitles" :key="index">
          {{ title }}
        </li>
      </ul>
    </div>

    <!-- Game UI Section -->
    <div class="container">
      <div class="day-counter">Day <span>{{ currentDay }}</span> / 10</div>
      <div class="game-container">
        <div class="balance-panel">
          <h3>Account Balance</h3>
          <div class="balance-info">Cash: ₩<span>{{ cash }}</span></div>
          <div class="balance-info">Portfolio Value: ₩<span>{{ portfolioValue }}</span></div>
          <div class="balance-info">Total Value: ₩<span>{{ totalValue }}</span></div>
          <h3 class="final-score" v-if="finalTotalValue !== 0">최종 금액은 {{ finalTotalValue }}원 입니다.</h3>
        </div>

        <div class="container">
          <div class="row">
            <div class="chart-section col-8">
              <canvas id="chart"></canvas>
            </div>
            <div class="col-4">
              <!-- Trading Panel -->
              <div class="trading-panel">
                <select v-model="selectedStock" @change="updateStockUrl">
                  <option value='삼성에스디에스'>삼성에스디에스</option>
                  <option value='넥슨게임즈'>넥슨게임즈</option>
                  <option value='카카오'>카카오</option>
                  <option value='NAVER'>NAVER</option>
                  <option value='CJ제일제당'>CJ제일제당</option>
                  <option value='농심'>농심</option>
                  <option value='하이트진로'>하이트진로</option>
                  <option value='오뚜기'>오뚜기</option>
                  <option value='SK텔레콤'>SK텔레콤</option>
                  <option value='KT'>KT</option>
                  <option value='삼성바이오로직스'>삼성바이오로직스</option>
                  <option value='셀트리온'>셀트리온</option>
                  <option value='오리엔트바이오'>오리엔트바이오</option>
                  <option value='미래에셋생명'>미래에셋생명</option>
                  <option value='삼보산업'>삼보산업</option>
                  <option value='한화생명'>한화생명</option>
                  <option value='현대차'>현대차</option>
                  <option value='기아'>기아</option>
                  <option value='한국전력'>한국전력</option>
                  <option value='POSCO홀딩스'>POSCO홀딩스</option>
                  <option value='삼성전자'>삼성전자</option>
                  <option value='SK하이닉스'>SK하이닉스</option>
                  <option value='YG PLUS'>YG PLUS</option>
                  <option value='JYP Ent.'>JYP Ent.</option>
                  <option value='에스엠'>에스엠</option>
                  <option value='CJ CGV'>CJ CGV</option>
                  <option value='GS건설'>GS건설</option>
                  <option value='KD'>KD</option>
                  <option value='대한항공'>대한항공</option>
                  <option value='CJ대한통운'>CJ대한통운</option>
                  <option value='제주항공'>제주항공</option>
                  <option value='SK이노베이션'>SK이노베이션</option>
                  <option value='S-Oil'>S-Oil</option>
                  <option value='롯데케미칼'>롯데케미칼</option>
                  <option value='LG화학'>LG화학</option>
                  <option value='에스에너지'>에스에너지</option>
                  <option value='메가스터디교육'>메가스터디교육</option>
                  <option value='웅진씽크빅'>웅진씽크빅</option>
                  <option value='KB금융'>KB금융</option>
                  <option value='우리금융지주'>우리금융지주</option>
                </select>

                <div class="stock-info">
                  <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>
                  <p>Max Buyable Shares: {{ maxBuyableShares }}</p>
                </div>

                <input 
                  type="number" 
                  v-model.number="tradeVolume" 
                  @input="validateInput"
                  placeholder="Enter quantity"
                />
                <div class="trade-buttons">
                  <button class="trade-button" @click="executeTrade('buy')">Buy</button>
                  <button class="trade-button" @click="executeTrade('sell')">Sell</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Portfolio Section -->
        <div class="portfolio">
          <h3>Your Holdings</h3>
          <div>
            <template v-for="(quantity, stock) in portfolio" :key="stock">
              <div v-if="quantity > 0">
                {{ stock }}: {{ quantity }} shares
              </div>
            </template>
          </div>
        </div>
        <button @click="nextDay">Next Day</button>
      </div>
    </div>
  </div>
</template>

<script setup>
/* --------------------------- Imports --------------------------- */
import { ref, computed, onMounted, watch } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import axios from 'axios';
import Chart from 'chart.js/auto';
// import api from '@/api';

/* --------------------------- State --------------------------- */
const stockStore = useStockStore();
const currentDay = ref(1);
const cash = ref(10000000);
const portfolio = ref({});
const selectedStock = ref('삼성에스디에스');
const tradeVolume = ref(0);
const startDate = ref('');
const finalTotalValue = ref(0);
const newsTitles = ref([]);
const stockData = ref({
    // 각 주식에 대한 가격 데이터 저장
    '삼성에스디에스' : [],
    '넥슨게임즈' : [],
    '카카오' : [],
    'NAVER' : [],
    'CJ제일제당' : [],
    '농심' : [],
    '하이트진로' : [],
    '오뚜기' : [],
    'SK텔레콤' : [],
    'KT' : [],
    '삼성바이오로직스' : [],
    '셀트리온' : [],
    '오리엔트바이오' : [],
    '미래에셋생명' : [],
    '삼보산업' : [],
    '한화생명' : [],
    '현대차' : [],
    '기아' : [],
    '한국전력' : [],
    '삼성전자' : [],
    'POSCO홀딩스' : [],
    'SK하이닉스' : [],
    'YG PLUS' : [],
    'JYP Ent.' : [],
    '에스엠' : [],
    'CJ CGV' : [],
    'GS건설' : [],
    'KD' : [],
    '대한항공' : [],
    'CJ대한통운' : [],
    '제주항공' : [],
    'SK이노베이션' : [],
    'S-Oil' : [],
    '롯데케미칼' : [],
    'LG화학' : [],
    '에스에너지' : [],
    '메가스터디교육' : [],
    '웅진씽크빅' : [],
    'KB금융' : [],
    '우리금융지주' : [],
});

/* --------------------------- Computed Values --------------------------- */
const formattedDate = computed(() => {
  if (!startDate.value) return '';
  const date = new Date(startDate.value);
  date.setDate(date.getDate() + currentDay.value - 1);
  return date.toISOString().split('T')[0];
});
const portfolioValue = computed(() => {
  return Object.keys(portfolio.value).reduce((total, stock) => {
    return total + (portfolio.value[stock] * (stockData.value[stock]?.[currentDay.value - 1]?.open_price || 0));
  }, 0);
});
const totalValue = computed(() => cash.value + portfolioValue.value);
const currentPrice = computed(() => stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price || 0);
const maxBuyableShares = computed(() => (currentPrice.value > 0 ? Math.floor(cash.value / currentPrice.value) : 0));

/* --------------------------- Functions --------------------------- */
// Random Date Fetch
async function fetchRandomDate() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/stocks/generate_random_date/');
    if (response.data.status === 'success') {
      startDate.value = response.data.start_date;
    } else {
      console.error('Error generating random date:', response.data.message);
    }
  } catch (error) {
    console.error('Error generating random date:', error);
  }
}

// Stock API Fetch
async function fetchStockData(apiUrl) {
  try {
    const response = await axios.get(apiUrl);
    if (response.data.status === 'success') {
      stockData.value[selectedStock.value] = response.data.data.map(item => ({
        open_price: item.open_price,
        close_price: item.close_price,
      }));
      updateChart();
    } else {
      console.error('Error fetching stock data:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
}

// News Titles Fetch
async function fetchNewsTitles() {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/stocks/fetch-news/?date=${formattedDate.value}`);
    if (response.data.status === 'success') {
      newsTitles.value = response.data.titles;
    } else {
      console.error('Error fetching news:', response.data.message);
    }
  } catch (error) {
    console.error('Failed to fetch news titles:', error);
  }
}

// Update Stock URL
function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];
  if (stockCode) {
    const apiUrl = `http://127.0.0.1:8000/api/stocks/${stockCode}/?start_date=${startDate.value}`;
    fetchStockData(apiUrl);
  }
}

// Chart Initialization
let chart;
function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`),
      datasets: [
        {
          label: 'Stock Price',
          data: stockData.value[selectedStock.value]?.slice(0, currentDay.value).map(item => item.open_price) || [],
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: { scales: { y: { beginAtZero: false } } },
  });
}

// Update Chart
function updateChart() {
  chart.data.datasets[0].data = stockData.value[selectedStock.value]?.map(item => item.open_price).slice(0, currentDay.value) || [];
  chart.update();
}

// Validate Trade Input
function validateInput(event) {
  const value = Number(event.target.value);
  tradeVolume.value = isNaN(value) || value < 0 ? 0 : value;
}

// Execute Trade
function executeTrade(type) {
  const volume = tradeVolume.value;
  const price = currentPrice.value;

  if (type === 'buy' && volume > 0 && cash.value >= price * volume) {
    cash.value -= price * volume;
    portfolio.value[selectedStock.value] = (portfolio.value[selectedStock.value] || 0) + volume;
  } else if (type === 'sell' && volume > 0 && (portfolio.value[selectedStock.value] || 0) >= volume) {
    cash.value += price * volume;
    portfolio.value[selectedStock.value] -= volume;
  } else {
    alert('Invalid trade!');
  }

  tradeVolume.value = 0;
}

// Next Day
function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;
    fetchNewsTitles();
    updateChart();
  } else {
    const finalPortfolioValue = Object.keys(portfolio.value).reduce((total, stock) => {
      const closePrice = stockData.value[stock]?.[9]?.close_price || 0;
      return total + (portfolio.value[stock] * closePrice);
    }, 0);
    finalTotalValue.value = cash.value + finalPortfolioValue;
    alert(`Game over. Your final total is ₩${finalTotalValue.value}`);
  }
}

/* --------------------------- Lifecycle --------------------------- */
onMounted(async () => {
  await fetchRandomDate();
  updateStockUrl();
  fetchNewsTitles();
  initializeChart();
});
watch([cash, portfolio, currentDay, selectedStock], updateChart);
</script>

<style scoped>
.trade-button { margin-right: 10px; }
.final-score { margin-top: 20px; color: red; }
</style>
