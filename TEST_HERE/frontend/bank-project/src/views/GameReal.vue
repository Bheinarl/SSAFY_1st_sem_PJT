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
                  
                  <br>
                  <div class="stock-info">
                    <br>
                    <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>
                    <br>
                  </div>

                  <!-- 기존 코드 -->
                  <!-- <input type="number" v-model.number="tradeVolume" placeholder="Enter quantity"> -->

                  <!-- 음수 및 문자 입력 방지 -->
                  <input 
                    type="number" 
                    v-model.number="tradeVolume" 
                    @input="validateInput"
                    placeholder="Enter quantity"
                  />


                  <div class="trade-buttons">
                    <br>
                    <button class="trade-button" @click="executeTrade('buy')">Buy</button>
                    <button class="trade-button" @click="executeTrade('sell')">Sell</button>
                    <br>
                  </div>
                </div>

              <div class="portfolio">
                <br>
                <h3>Your Holdings</h3>
                <div>
                  <!-- 0 shares 는 표시하지 않도록 변경 -->
                  <template v-for="(quantity, stock) in portfolio" :key="stock">
                    <div v-if="quantity > 0">
                      {{ stock }}: {{ quantity }} shares
                      <br>
                    </div>
                  </template>
                </div>
              </div>

              <button @click="nextDay">Next Day</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import axios from 'axios';
import Chart from 'chart.js/auto';
// import api from '@/api';

// 주식 데이터 저장소 사용
const stockStore = useStockStore();

// 상태 관리 변수
const currentDay = ref(1);  // 현재 날짜 (1~10일)
const cash = ref(10000000); // 초기 현금 (₩10,000,000)
const portfolio = ref({});  // 보유 주식 정보 (주식 이름: 수량)
const selectedStock = ref('삼성에스디에스');  // 선택된 주식
const tradeVolume = ref(0); // 거래량 (사용자 입력)
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

let chart; // 차트를 저장할 변수
const finalTotalValue = ref(0); // 게임 종료 후 최종 자산

// 계산된 값
const portfolioValue = computed(() => {
  // 포트폴리오의 총 가치를 계산 (보유 주식 * 현재 주가)
  return Object.keys(portfolio.value).reduce((total, stock) => {
    return total + (portfolio.value[stock] * (stockData.value[stock]?.[currentDay.value - 1]?.open_price || 0));
  }, 0);
});

const totalValue = computed(() => {
  // 총 자산 = 현금 + 포트폴리오 가치
  return cash.value + portfolioValue.value;
});

const currentPrice = computed(() => {
  // 선택된 주식의 현재 가격
  return stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price || 0;
});


// 주식 데이터 업데이트 URL 설정
function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];  // 선택된 주식의 코드 가져오기
  if (stockCode) {
    const apiUrl = `http://127.0.0.1:8000/api/stocks/${stockCode}/`; // API URL 생성
    console.log('API URL:', apiUrl); 
    fetchStockData(apiUrl); // 주식 데이터 가져오기
  }
}

// 음수 및 문자 입력 방지 함수
function validateInput(event) {
  const value = event.target.value; // 실제 입력된 값을 가져옴
  // 숫자가 아니거나 음수라면 초기화
  if (isNaN(Number(value)) || Number(value) < 0) {
    tradeVolume.value = 0;
  } else {
    tradeVolume.value = Number(value); // 유효한 숫자면 반영
  }
}

// API에서 주식 데이터 가져오기
async function fetchStockData(apiUrl) {
  try {
    const response = await axios.get(apiUrl); // Axios를 사용해 API 호출
    console.log('API Response:', response); // 응답 데이터 확인(디버깅용)
    if (response.data.status === 'success') {
      stockData.value[selectedStock.value] = response.data.data.map(item => ({
        open_price: item.open_price,
        close_price: item.close_price
      })); // 주식 데이터 저장
      updateChart(); // 차트 업데이트
    } else {
      console.error('Error fetching stock data:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error); // 에러 처리
  }
}

// 차트 초기화
function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d'); // 차트 캔버스 컨텍스트 가져오기
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 10 }, (_, i) => `Day ${i + 1}`), // X축: Day 1 ~ 10
      datasets: [{
        label: 'Stock Price',
        data: stockData.value[selectedStock.value].slice(0, currentDay.value), // 주가 데이터
        borderColor: 'rgba(75, 192, 192, 1)',  // 선 색상
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false  
        }, // Y축 시작점 설정
      }
    }
  });
}

// 차트 업데이트
function updateChart() {
  chart.data.datasets[0].data = stockData.value[selectedStock.value].map(item => item.open_price).slice(0, currentDay.value); // 차트에 데이터 반영
  chart.update(); // 차트 업데이트
}

// 거래 함수 (매수/매도)
function executeTrade(type) {
  const volume = tradeVolume.value; // 거래량
  const price = currentPrice.value; // 현재 주가
  if (type === 'buy') {
    if (cash.value >= price * volume) {
      cash.value -= price * volume; // 현금 감소
      portfolio.value[selectedStock.value] = (portfolio.value[selectedStock.value] || 0) + volume;
    } else {
      alert('Not enough cash'); // 현금 부족 경고
    }
  } else if (type === 'sell') {
    if ((portfolio.value[selectedStock.value] || 0) >= volume) {
      cash.value += price * volume; // 현금 증가
      portfolio.value[selectedStock.value] -= volume; // 주식 감소
    } else {
      alert('Not enough shares'); // 주식 부족 경고
    }
  }
}

// 다음 날짜로 진행
function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;  // 날짜 증가
    updateChart(); // 차트 업데이트
  } else {
    // 게임 종료 및 최종 자산 계산
    console.log('stockData는 이렇게 출력됩니다.', stockData.value);
    const finalPortfolioValue = Object.keys(portfolio.value).reduce((total, stock) => {
      const closePrice = stockData.value[stock]?.[9]?.close_price || 0; // 10일차 close_price 사용
      return total + (portfolio.value[stock] * closePrice);
    }, 0);
    finalTotalValue.value = cash.value + finalPortfolioValue; // 최종 자산 계산
    console.log('Cash:', cash.value);
    console.log('Final Portfolio Value:', finalPortfolioValue);
    console.log('Final Total Value:', finalTotalValue.value);
    alert(`Game over. Your total value is ₩${finalTotalValue.value}`);
  }
}

// 컴포넌트 초기화 시 호출
onMounted(() => {
  updateStockUrl(); // 초기 데이터 가져오기
  fetchStockData(); // API 호출
  initializeChart(); // 차트 초기화
  updateChart(); // 차트 업데이트
});


// Watchers to update the UI when values change
// 값 변경 감지 및 업데이트
watch([cash, portfolio, currentDay, selectedStock], () => {
  updateChart(); // 상태 변경 시 차트 업데이트
});



</script>

<style scoped>
/* .chart-section {
  width: 80%;
  height: 300px;
  margin: 0 auto;
} */

.trade-button {
  margin-right: 10px;
}

.final-score {
  margin-top: 20px;
  color: red;
}
</style>