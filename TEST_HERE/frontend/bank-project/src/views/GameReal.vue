<template>
  <div>
    <!-- Header Section -->
    <div class="header">
      <div class="container">
        <h1>10-Day Stock Investment Game</h1>
      </div>
    </div>

    <!-- News Section -->
    <div class="news-container" v-if="currentDay < 11">
      <h3>Latest News</h3>

      <ul>
        <!-- 최대 10개까지만 출력 -->
        <li v-for="(title, index) in newsTitles" :key="index">
          {{ title }}
        </li>
        <!-- 뉴스가 없을 경우에는 No news available for this date. 메시지가 표시 -->
        <h5 v-if="newsTitles.length === 0">해당 날짜의 뉴스를 로딩 중입니다.</h5>
      </ul>

      

    </div>

    <!-- Game UI Section -->
    <div class="container">
      <div class="day-counter"  v-if="currentDay < 11">Day <span>{{ currentDay }}</span> / 10</div>
      <div class="day-counter"  v-if="currentDay > 10">Day <span>10</span> / 10</div>

      
        <div class="game-container">
          
          <table class="table align-middle entire-earning-rate" style="margin: 10px;">
            <tr>
              <th>전체 수익률</th>
              <th>평가 손익</th>
              <th>잔고 평가</th>
              <th>시드 머니</th>
              <th>주문 가능</th>
              <th>추정 자산</th>
            </tr>
            <tr>
              <td :class="{'color-red': totalEarningRate > 0, 'color-blue': totalEarningRate < 0}">{{ totalEarningRate.toFixed(2) }}%</td>
              <td :class="{'color-red': totalEvaluationProfit > 0, 'color-blue': totalEvaluationProfit < 0}">{{ totalEvaluationProfit }}</td>
              <td>{{ portfolioValue }}</td>
              <td>{{ seedMoney }}</td>
              <td>{{ cash }}</td>
              <td>{{ totalValue }}</td>
            </tr>
          </table>
          
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

                  <div>
                    <!-- 주식 정보 -->
                    <div class="stock-info">
                      <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>
                      <h4 v-if="beforePrice > 0" class="color-red">▲ {{ beforePrice }}</h4>
                      <h4 v-if="beforePrice === 0">---</h4>
                      <h4 v-if="beforePrice < 0" class="color-blue">▼ {{ -beforePrice }}</h4>
                      <p v-if="currentDay < 11">Max Buyable Shares: {{ maxBuyableShares }}</p> <!-- 최대 매수 가능 수량 -->
                      <!-- <p>Max Sellable Shares: {{ maxSellableShares }}</p> 최대 매도 가능 수량 -->
                    </div>

                    <!-- 매수/매도량 입력 -->
                    <input 
                      type="number" 
                      v-model.number="tradeVolume" 
                      @input="validateInput"
                      placeholder="Enter quantity"
                      v-if="currentDay < 11"
                    />

                    <!-- 거래 버튼 -->
                    <div class="trade-buttons" style="margin-top: 5px;"  v-if="currentDay < 11">
                      <button class="trade-button" @click="executeTrade('buy')" v-if="currentPrice !== 0">Buy</button>
                      <button class="trade-button" v-else>Buy</button>
                      <button class="trade-button" @click="executeTrade('sell')"v-if="currentPrice !== 0">Sell</button>
                      <button class="trade-button" v-else>Sell</button>
                      
                    </div>
                  </div>

                </div>

              <div class="portfolio">
                <br>
                <h3>Your Holdings</h3>
                <div>
                  <!-- 0 shares 는 표시하지 않도록 변경 -->
                  <template v-for="key in Object.keys(portfolio)" :key="key">
                    <div v-if="totalQuantity[key] > 0">
                      {{ key }}: {{ totalQuantity[key] }} shares  <span v-if="keyBeforePrice[key] > 0" class="color-red">▲{{ keyBeforePrice[key] }}</span><span v-if="keyBeforePrice[key] === 0">--</span><span v-if="keyBeforePrice[key] < 0" class="color-blue">▼{{ -keyBeforePrice[key] }}</span>
                      <br>
                    </div>
                  </template>
                </div>
              </div>
              <button v-if="currentDay < 11 && currentPrice === 0">Next Day</button>
              <button @click="nextDay" v-else-if="currentDay < 11">Next Day</button>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <table class="table align-middle entire-earning-rate" style="margin: 10px;">
    <thead>
      <tr>
        <th>종목</th>
        <th>보유량</th>
        <th>매입 단가</th>
        <th>평가 금액</th>
        <th>평가 손익</th>
        <th>수익률</th>
      </tr>
    </thead>

    <tbody>
      <template v-for="key in Object.keys(portfolio)" :key="key">
        <tr v-if="totalQuantity[key] !== 0">
          <td>{{ key }}</td>
          <td>{{ totalQuantity[key] }}</td>
          <td>{{ purchasePrice[key].toFixed(0) }}</td>
          <td>{{ evaluationPrice[key].toFixed(0) }}</td>
          <td :class="{'color-red': evaluationProfit[key] > 0, 'color-blue': evaluationProfit[key] < 0}">{{ evaluationProfit[key].toFixed(0) }}</td>
          <td :class="{'color-red': earningRate[key] > 0, 'color-blue': earningRate[key] < 0}">{{ earningRate[key].toFixed(2) }}</td>
        </tr>
      </template>
    </tbody>
  </table>
</template>

<script setup>
/* --------------------------- Imports --------------------------- */
import { ref, computed, onMounted, watch } from 'vue';
import { addDays, format } from 'date-fns';
import { useStockStore } from '@/stores/StockStore';
import axios from 'axios';
import Chart from 'chart.js/auto';
// import api from '@/api';

/* --------------------------- State --------------------------- */
const stockStore = useStockStore();


// 상태 관리 변수
const currentDay = ref(1);  // 현재 날짜 (1~10일)
const seedMoney = 10000000
const cash = ref(10000000); // 초기 현금 (₩10,000,000)
const portfolio = ref({});  // 보유 주식 정보 (주식 이름: 수량)
const selectedStock = ref('삼성에스디에스');  // 선택된 주식
const tradeVolume = ref(0); // 거래량 (사용자 입력)
const startDate = ref(''); // 난수로 받을 시작 날짜

const finalTotalValue = ref(0);
const newsTitles = ref([]);


const stockData = ref({
    // 각 주식에 대한 가격 데이터 저장
    '삼성에스디에스' : [], '넥슨게임즈' : [], '카카오' : [], 'NAVER' : [],
    'CJ제일제당' : [], '농심' : [], '하이트진로' : [], '오뚜기' : [],
    'SK텔레콤' : [], 'KT' : [], '삼성바이오로직스' : [], '셀트리온' : [],
    '오리엔트바이오' : [], '미래에셋생명' : [], '삼보산업' : [], '한화생명' : [],
    '현대차' : [], '기아' : [], '한국전력' : [], '삼성전자' : [],
    'POSCO홀딩스' : [], 'SK하이닉스' : [], 'YG PLUS' : [], 'JYP Ent.' : [],
    '에스엠' : [], 'CJ CGV' : [], 'GS건설' : [], 'KD' : [],
    '대한항공' : [], 'CJ대한통운' : [], '제주항공' : [], 'SK이노베이션' : [],
    'S-Oil' : [], '롯데케미칼' : [], 'LG화학' : [], '에스에너지' : [],
    '메가스터디교육' : [], '웅진씽크빅' : [], 'KB금융' : [], '우리금융지주' : [],
});

/* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 시작 @@@@@@@@@@@@@@@@@@@ */
const tradePattern = ref({
  totalTrades: 0,          // 총 거래 횟수
  buyCount: 0,             // 매수 횟수
  sellCount: 0,            // 매도 횟수
  holdingPeriod: [],       // 평균 보유 기간
  riskLevel: 0,            // 위험 선호도
  sectorPreference: {},    // 선호 업종
  reactionToNews: 0        // 뉴스 반응도 // 이건 긍정적, 부정적 뉴스 키워드 반응
});

/* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 끝 @@@@@@@@@@@@@@@@@@@ */

/* --------------------------- Computed Values --------------------------- */

const portfolioValue = computed(() => {

  return Object.keys(portfolio.value).reduce((total, stock) => {
    const totalQuantity = portfolio.value[stock].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0); // totalQuantity는 총 보유 수량
    // 포트폴리오 가치 계산: (현재 주가 * 보유 수량)
    if (currentDay.value > 10) {
      const currentPrice = stockData.value[stock][9]?.close_price || 0;
      return total + (currentPrice * totalQuantity);
    } else {
      const currentPrice = stockData.value[stock]?.[currentDay.value - 1]?.open_price || 0;
      return total + (currentPrice * totalQuantity);
    }
  }, 0);
});

const maxBuyableShares = computed(() => (currentPrice.value > 0 ? Math.floor(cash.value / currentPrice.value) : 0));


const totalValue = computed(() => {
  // 총 자산 = 현금 + 포트폴리오 가치
  return cash.value + portfolioValue.value;
});

const currentPrice = computed(() => {
  // 선택된 주식의 현재 가격
  if (currentDay.value > 10) {
    return stockData.value[selectedStock.value][9]?.close_price || 0;
  } else {
    return stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price || 0;
  }
});

const beforePrice = computed(() => {
  // 선택된 주식의 현재 가격
  if (currentDay.value === 1) {
    return 0;
  } else if (currentDay.value > 10) {
  return stockData.value[selectedStock.value][9]?.close_price - stockData.value[selectedStock.value][9]?.open_price;
  } else {
    return stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price - stockData.value[selectedStock.value][currentDay.value - 2]?.open_price;
  }
});

const keyBeforePrice = computed(() => {
  // 선택된 주식의 현재 가격
  const result = {}
  for (const key in portfolio.value) {
    if (currentDay.value === 1) {
      result[key] = 0;
    } else if (currentDay.value > 10) {
      result[key] = stockData.value[key][9]?.close_price - stockData.value[key][9]?.open_price;
    } else {
      result[key] = stockData.value[key]?.[currentDay.value - 1]?.open_price - stockData.value[key][currentDay.value - 2]?.open_price;
    }
  }
  return result
});

const totalEarningRate = computed(() => {
  // 전체 수익률 계산
  console.log('totalValue.value는 이렇게 출력됩니다.', totalValue.value);
  console.log('seedMoney는 이렇게 출력됩니다.', seedMoney);
  return ((totalValue.value / seedMoney) - 1) * 100;
});

const totalEvaluationProfit = computed(() => {
  // 평가 손익 = 평가 금액 - 총 매입 금액 (FIFO 방식 적용)
  return portfolioValue.value - Object.keys(portfolio.value).reduce((total, stock) => {
    const transactions = portfolio.value[stock].transactions; // 거래 내역
    let remainingQuantity = portfolio.value[stock].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량을 따로 변수로 추적
    let totalPurchaseAmount = 0; // 총 매입 금액

    // FIFO 방식으로 매입 금액 계산
    for (let i = 0; i < transactions.length; i++) {
      const transaction = transactions[i];
      if (remainingQuantity <= 0) break; // 남은 수량이 없으면 종료

      const purchaseQuantity = Math.min(transaction.quantity, remainingQuantity); // 매도할 수 있는 수량만큼
      totalPurchaseAmount += purchaseQuantity * transaction.price; // 매입 금액 누적
      remainingQuantity -= purchaseQuantity; // 남은 수량 업데이트
    }

    return total + totalPurchaseAmount; // 총 매입 금액 계산
  }, 0);
});

const totalQuantity = computed(() => {
  // 해당 주식의 총 수량
  const result = {}
  for (const key in portfolio.value) {
    result[key] = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
  }
  return result
});

const purchasePrice = computed(() => {
  // 매입 단가 계산 = 총 매입 금액 / 보유 수량
  const result = {}
  for (const key in portfolio.value) {
    const transactions = portfolio.value[key].transactions;  // 해당 종목의 거래 내역
    let remainingQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량
    let totalPurchaseAmount = 0;  // 총 매입 금액

    // FIFO 방식으로 매입 금액 계산
    for (let i = 0; i < transactions.length; i++) {
      const transaction = transactions[i];
      if (remainingQuantity <= 0) break;  // 남은 수량이 없으면 종료

      const purchaseQuantity = Math.min(transaction.quantity, remainingQuantity);  // 매도할 수 있는 수량만큼
      totalPurchaseAmount += purchaseQuantity * transaction.price;  // 매입 금액 누적
      remainingQuantity -= purchaseQuantity;  // 남은 수량 업데이트
    }

    // 매입단가는 총 매입 금액 / 보유 수량으로 계산
    result[key] = totalPurchaseAmount / (portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0));
  }
  return result
});

const evaluationPrice = computed(() => {
  // 평가 금액 계산 = 현재 가격 * 보유 수량
  const result = {}
  for (const key in portfolio.value) {
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량
    if (currentDay.value > 10) {
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = selectedQuantity * selectedPrice
    } else {
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = selectedQuantity * selectedPrice
    }
    console.log('evaluationPrice의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})

const evaluationProfit = computed(() => {
  // 평가 손익 계산 = 평가 금액 - 총 매입 금액
  const result = {}
  for (const key in portfolio.value) {
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량
    const selectedTransaction = portfolio.value[key].transactions.reduce((totalTransaction, transaction) => totalTransaction + (transaction.quantity * transaction.price), 0);
    if (currentDay.value > 10) {
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = selectedQuantity * selectedPrice - selectedTransaction
    } else {
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = selectedQuantity * selectedPrice - selectedTransaction
    }
    console.log('evaluationProfit의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})

const earningRate = computed(() => {
  // 수익률 계산 = 평가 금액 / 총 거래 금액 - 1
  const result = {}
  for (const key in portfolio.value) {
    // const selectedQuantity = portfolio.value[key]?.quantity
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
    const selectedTransaction = portfolio.value[key].transactions.reduce((totalTransaction, transaction) => totalTransaction + (transaction.quantity * transaction.price), 0);
    if (currentDay.value > 10) {
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = (selectedQuantity * selectedPrice) / selectedTransaction - 1
    } else {
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = (selectedQuantity * selectedPrice) / selectedTransaction - 1
    }
    console.log('earningRate의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})


/* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 시작 @@@@@@@@@@@@@@@@@@@ */
const calculateRiskLevel = computed(() => {
  const { buyCount, sellCount, holdingPeriod } = tradePattern.value;

  // 1. 거래 빈도와 평균 보유 기간 계산
  const tradingFrequency = (buyCount + sellCount) / currentDay.value;
  const avgHoldingPeriod =
    holdingPeriod.length > 0
      ? holdingPeriod.reduce((a, b) => a + b, 0) / holdingPeriod.length
      : 0;

  // 2. 재무자산 비율 계산
  const totalAssets = cash.value + portfolioValue.value; // 총 자산
  const financialAssetsRatio = portfolioValue.value / totalAssets; // 재무자산 비율
  console.log(
    "Risk Level Debug:",
    `Trading Frequency: ${tradingFrequency}, Avg Holding Period: ${avgHoldingPeriod}, Financial Assets Ratio: ${financialAssetsRatio}`
  );

  // 3. 위험 선호도 계산 (0~1 사이 값)
  // 가중치를 조절하여 각 항목의 중요도를 반영
  return (
    tradingFrequency * 0.3 + // 거래 빈도에 30% 반영
    (1 - avgHoldingPeriod / 10) * 0.4 + // 보유 기간에 40% 반영
    financialAssetsRatio * 0.3 // 재무자산 비율에 30% 반영
  );
});



/* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 끝 @@@@@@@@@@@@@@@@@@@ */


/* --------------------------- Functions --------------------------- */
// Random Date Fetch

async function fetchRandomDate() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/stocks/generate_random_date/');
    if (response.data.status === 'success') {
      startDate.value = response.data.start_date;
      await updateStockUrl()
    } else {
      console.error('Error generating random date:', response.data.message);
    }
  } catch (error) {
    console.error('Error generating random date:', error);
  }
}

async function fetchStockData(apiUrl) {
  try {
    const response = await axios.get(apiUrl);
    if (response.data.status === 'success') {
      // API로부터 받은 데이터를 저장
      stockData.value[selectedStock.value] = response.data.data.map(item => ({
        date: item.date,
        open_price: item.open_price,
        close_price: item.close_price,
      }));
      console.log('stockData는 이렇게 출력됩니다.', stockData.value);
      updateChart();
    } else {
      console.error('Error fetching stock data:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
}

// Update Stock URL
async function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];
  if (stockCode) {
    const apiUrl = `http://127.0.0.1:8000/api/stocks/find_stock_data/${stockCode}/?start_date=${startDate.value}`;
    console.log("apiUrl : ",apiUrl)

    fetchStockData(apiUrl);
  }
}

async function updateNews() {
  const currentDate = ref(startDate.value);
  console .log('currentDate는 이렇게 출력됩니다.111', currentDate.value);
  if (startDate.value != stockData.value['삼성에스디에스']?.[currentDay.value - 1]?.date) {
    currentDate.value = stockData.value['삼성에스디에스']?.[currentDay.value - 1]?.date
    console .log('currentDate는 이렇게 출력됩니다.222', currentDate.value);
  }
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/stocks/fetch_news/?start_date=${currentDate.value}`);
    if (response.data.status === 'success') {
      newsTitles.value = response.data.data;
    } else {
      console.error('Error updateNews11:', response.data.message);
    }
  } catch (error) {
    console.error('Error updateNews22:', error);
  }
}

// 페이지 로딩 후 2초 뒤에 updateNews 함수 실행
setTimeout(() => {
  updateNews();
}, 2000);  // 2000ms = 2초

// Chart Initialization
let chart;
function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: Array.from({ length: 11 }, (_, i) => (i === 10 ? '최종 결과' : `Day ${i + 1}`)), // X축: Day 1 ~ 10
      datasets: [{
        label: 'Stock Price',
        data: stockData.value[selectedStock.value].slice(0, currentDay.value), // 주가 데이터
        borderColor: 'rgba(75, 192, 192, 1)',  // 선 색상
        borderWidth: 1
      }]
    },
    options: { scales: { y: { beginAtZero: false } } },
  });
}

// Update Chart
function updateChart() {
  const data = stockData.value[selectedStock.value].map(item => item.open_price).slice(0, currentDay.value);
  if (currentDay.value >= 10) {
    data[currentDay.value - 1] = stockData.value[selectedStock.value][currentDay.value - 2].close_price;
  }
  chart.data.datasets[0].data = data; // 차트에 데이터 반영
  chart.update(); // 차트 업데이트
}




// Next Day 다음 날짜로 진행
async function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;
    updateChart(); // 차트 업데이트
    updateNews();
  } else {
    // 게임 종료 및 최종 자산 계산
    currentDay.value++; // 마지막 날짜까지 진행
    updateChart(); // 차트 업데이트
    console.log('stockData는 이렇게 출력됩니다.', stockData.value);

    const finalPortfolioValue = Object.keys(portfolio.value).reduce((total, stock) => {
      const closePrice = stockData.value[stock]?.[9]?.close_price || 0; // 10일차 close_price 사용
      const selectedQuantity = portfolio.value[stock].transactions.reduce(
        (totalQuantity, transaction) => totalQuantity + transaction.quantity,0);  // 보유 수량
        return total + (selectedQuantity * closePrice);
    }, 0);
    finalTotalValue.value = cash.value + finalPortfolioValue; // 최종 자산 계산
    console.log('Cash:', cash.value);
    console.log('Final Portfolio Value:', finalPortfolioValue);
    console.log('Final Total Value:', finalTotalValue.value);


    // 🔥 보유 기간 업데이트 (마지막 날까지 보유한 주식 포함)
    Object.keys(portfolio.value).forEach((stock) => {
      const transactions = portfolio.value[stock].transactions;
      transactions.forEach((transaction) => {
        const holdingDays = 10 - transaction.day; // 마지막 날(10일) 기준 보유 기간 계산
        tradePattern.value.holdingPeriod.push(holdingDays); // 보유 기간 기록
      });
    });
    console.log('Updated holdingPeriod:', tradePattern.value.holdingPeriod);



    const response = await fetch('http://127.0.0.1:8000/accounts/update_max_score/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`, // 토큰을 헤더에 포함
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ max_score: finalTotalValue.value }) // 최종 자산을 서버로 전송
    });

    alert(`Game over. Your total value is ₩${finalTotalValue.value}`); 
    if (response.ok) {
      console.log('Game over. Your total value is ₩', finalTotalValue.value); 
    } else {
      console.error('Failed to update max score:', response.statusText);
    }


    /* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 시작 @@@@@@@@@@@@@@@@@@@ */
    const riskLevel = calculateRiskLevel.value;
    let investorType;
    console.log(riskLevel);
    if (riskLevel < 0.3) investorType = '안정 추구형';
    else if (riskLevel < 0.6) investorType = '균형 투자형';
    else if (riskLevel < 0.8) investorType = '공격 투자형';
    else investorType = '투기형';

    // 분석 결과 서버로 전송
    const analysisData = {
      investor_type: investorType,
      risk_level: riskLevel,
      trade_pattern: tradePattern.value,
      final_value: finalTotalValue.value
    };

    try {
      await axios.post('http://127.0.0.1:8000/api/analysis/save/', analysisData);
    } catch (error) {
      console.error('Failed to save analysis:', error);
    }

    alert(`게임 종료!\n최종 자산: ₩${finalTotalValue.value}\n투자자 유형: ${investorType}`);

    /* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 끝 @@@@@@@@@@@@@@@@@@@ */




  }

  if (currentDay.value === 10) {
    const investorType = analyzeInvestorType();
    const analysis = {
      type: investorType,
      pattern: tradePattern.value,
      finalValue: finalTotalValue.value
    };
    
    // 분석 결과 서버로 전송
    await axios.post('http://127.0.0.1:8000/api/analysis/save/', analysis);
    
    // 결과 표시
    showAnalysisResult(analysis); 
  }

}



/* --------------------------- Lifecycle --------------------------- */
onMounted(async () => {
  await fetchRandomDate();
  updateStockUrl();
  initializeChart();
  // updateNews();
});


// 입력값 검증 함수
function validateInput(event) {
  const value = Number(event.target.value); // 입력값을 숫자로 변환
  if (isNaN(value) || value < 0) {
    tradeVolume.value = 0; // 음수 또는 숫자가 아닌 경우 초기화
  } else {
    tradeVolume.value = value; // 유효한 값 반영
  }
}

// 거래 실행 함수 (매수/매도)
function executeTrade(type) {
  const volume = tradeVolume.value; // 거래량
  const price = currentPrice.value; // 현재 주가

  if (!portfolio.value[selectedStock.value]) {
    portfolio.value[selectedStock.value] = { transactions: [] }; // 매입 내역 배열로 관리
  }

  if (type === 'buy') {
    // 매수 조건: 현금이 충분하고, 거래량이 0보다 큼
    if (volume > 0 && cash.value >= price * volume) {
      cash.value -= price * volume; // 현금 감소

      // 매수 거래 내역 추가 (FIFO 방식 적용을 위해 배열에 추가)
      portfolio.value[selectedStock.value].transactions.push({
        quantity: volume,
        price: price,
        day: currentDay.value  // 거래 시점 추가
      });
      
      console.log(`매수 완료: ${volume}주, 가격: ${price}`);

      /* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 시작 @@@@@@@@@@@@@@@@@@@ */
      // console.log("사든 팔든 일단 이거 출력해라(사고있음)");
      // console.log("portfolio",portfolio);
      // console.log("portfolio.value",portfolio.value);
      // console.log("portfolio.value[selectedStock.value].transactions",portfolio.value[selectedStock.value].transactions);
      // console.log("tradePattern@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",tradePattern);
      // console.log("volume",volume);
      tradePattern.value.buyCount += volume;
      tradePattern.value.totalTrades += volume;
      // 업종 선호도 기록
      const sector = stockStore.stockSectors[selectedStock.value];
      tradePattern.value.sectorPreference[sector] = (tradePattern.value.sectorPreference[sector] || 0) + 1;
      // console.log("tradePattern@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",tradePattern);
      console.log("transactions 확인하기 : ", portfolio.value[selectedStock.value].transactions);
      /* @@@@@@@@@@@@@@@@@@@ 투자 유형 관련 수정 끝 @@@@@@@@@@@@@@@@@@@ */
    } else {
      alert('Not enough cash or invalid quantity for buying.'); // 에러 메시지
    }
  } else if (type === 'sell') {
  // 매도 조건: 보유 주식이 충분하고, 거래량이 0보다 큼
  const totalQuantityAvailable = portfolio.value[selectedStock.value].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);

  if (volume > 0 && totalQuantityAvailable >= volume) {
    let remainingQuantity = volume;
    let totalCost = 0;

    // FIFO 방식으로 매도
    while (remainingQuantity > 0) {
      const firstTransaction = portfolio.value[selectedStock.value].transactions[0]; // 가장 오래된 거래 내역

      if (!firstTransaction) {
        console.error('Error: No transaction found in portfolio for sell operation.');
        break;
      }

      // 보유 기간 계산 및 기록
      const holdingDays = currentDay.value - firstTransaction.day;
      tradePattern.value.holdingPeriod.push(holdingDays);

      if (firstTransaction.quantity <= remainingQuantity) {
        // 매도 수량이 해당 거래 내역의 수량보다 작거나 같으면 해당 거래 내역을 모두 소진
        totalCost += firstTransaction.quantity * firstTransaction.price;
        remainingQuantity -= firstTransaction.quantity;
        portfolio.value[selectedStock.value].transactions.shift(); // 해당 거래 내역 제거
      } else {
        // 매도 수량이 해당 거래 내역의 수량보다 크면 일부만 소진
        totalCost += remainingQuantity * firstTransaction.price;
        firstTransaction.quantity -= remainingQuantity;
        remainingQuantity = 0;
      }
      console.log("transactions 확인하기 : ", portfolio.value[selectedStock.value].transactions);

    }

    // 매도 완료 후 현금 증가
    cash.value += price * volume; // 현금 증가

    console.log(`매도 완료: ${volume}주, 가격: ${price}, 총 매도 금액: ${totalCost}`);

    // 매도 거래 횟수 업데이트
    tradePattern.value.sellCount += volume;
    tradePattern.value.totalTrades += volume;

    // console.log('tradePattern after sell:', tradePattern.value);
  } else {
    alert('Not enough shares to sell.');
  }
}

// 위험 선호도 계산
console.log("Calculating risk level...");
try {
  const riskLevel = calculateRiskLevel.value;
  tradePattern.value.riskLevel = riskLevel;
  console.log("Risk Level: ", riskLevel);
} catch (error) {
  console.error("Error accessing calculateRiskLevel: ", error);
}


// 거래 완료 후 입력값 초기화
tradeVolume.value = 0;

 
console.log('tradePattern@@@@@@@@@@@@@@', tradePattern.value);
} // executeTrade 함수 끝
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

.color-red {
  color: red;
}

.color-blue {
  color: blue;
}
</style>