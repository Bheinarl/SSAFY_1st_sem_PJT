<template>
  <header>
    <Navbar />
  </header>
  <div class="game-container">

    <!-- Sidebar Section -->
    <aside class="sidebar">
      <!-- 기존 사이드바 콘텐츠 유지 -->
      <h2 class="game-title">모의 투자 게임📈📉</h2>
      <h6>시드머니 천만원이 나에게 주어진다면?</h6>

      <!-- Day Counter -->
      <div class="day-container">
        <div v-if="currentDay < 11" class="progress-container">
          <div class="day-counter">
            <p class="dayyy" v-if="currentDay < 11">Day <span>{{ currentDay }}</span> / 10</p>
            <p class="dayyy" v-else>Day <span>10</span> / 10</p>
          </div>
          <div class="progress-bar">
            <div v-if="currentDay < 11" class="progress" :style="{ width: (currentDay / 10) * 100 + '%' }"></div>
            <div v-else class="progress" :style="{ width: 100 + '%' }"></div>
          </div>
          <br />

          <button v-if="currentDay < 11" @click="nextDay" class="next-day-btn">다음 날로 넘어가기 ⏩</button>
          <!--✅⏩ -->
        </div>

        <!-- Final Results -->
        <div v-if="currentDay > 10" class="final-results">
          <div class="result-item">💰최종 자산: <span>₩{{ finalTotalValue }}</span></div>
          <div class="result-item">👤투자자 유형:
            <span>{{ investorType }}</span>
            <span v-if="investorType === '안정 추구형'">😌</span>
            <span v-if="investorType === '균형 투자형'">🧐</span>
            <span v-if="investorType === '공격 투자형'">😏</span>
            <span v-if="investorType === '투기형'">🤑</span>
          </div>
          <div class="result-item">
            📆실제 주식 데이터 기간:
            <p>{{ startDateValue }} ~ {{ endDateValue }}</p>
          </div>
          <div class="result-buttons">
            <button @click="goFinanceRecommend" class="btn recommend-btn">펀드 상품 추천 바로가기</button>
            <button @click="restartGame" class="btn restart-btn">게임 다시 시작</button>
          </div>
        </div>
      </div>

      <!-- Portfolio Overview -->
      <table class="table portfolio-overview">
        <thead>
          <tr>
            <th colspan="2">📊 전체 포트폴리오 📊</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>전체 수익률</th>
            <td :class="{ 'positive': totalEarningRate > 0, 'negative': totalEarningRate < 0 }">
              {{ totalEarningRate.toFixed(2) }}%
            </td>
          </tr>
          <tr>
            <th>평가 손익</th>
            <td :class="{ 'positive': totalEvaluationProfit > 0, 'negative': totalEvaluationProfit < 0 }">
              {{ totalEvaluationProfit }}
            </td>
          </tr>
          <tr>
            <th>잔고 평가</th>
            <td>{{ portfolioValue }}</td>
          </tr>
          <tr>
            <th>시드 머니</th>
            <td>{{ seedMoney }}</td>
          </tr>
          <tr>
            <th>주문 가능</th>
            <td>{{ cash }}</td>
          </tr>
          <tr>
            <th>추정 자산</th>
            <td>{{ totalValue }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Additional Buttons -->
      <div class="button-group">
        <!-- <button @click="goToExchangeRateCalculator" class="btn">
          환율 계산기
        </button> -->

        <!-- 환율 계산기 버튼 -->
        <button @click="openModal" class="btn primary-btn">환율 계산기 열기🔢</button>
        <!-- 환율 계산기 모달 -->
        <Modal :isOpen="isModalOpen" @close="closeModal">
          <ExchangeRateAlert />
        </Modal>


        <button @click="goToLeaderboard" class="btn">
          랭킹 보러가기➰
        </button>
      </div>

    </aside>

    <!-- Main Content Section -->
    <section class="main-content">
      
      <!-- 뉴스와 차트: 1행 -->
      <div class="top-section">
        <div class="news-section">
          <h3>뉴스</h3>
          <ul>
            <li v-for="(title, index) in newsTitles" :key="index">{{ title }}</li>
            <h5 v-if="newsTitles.length === 0">해당 날짜의 뉴스를 로딩 중입니다.</h5>
          </ul>
        </div>
        <div class="charts-section">
          <h3>{{selectedStock}} 주식 차트</h3>
          <canvas id="chart"></canvas>
        </div>
      </div>

      <!-- 주식 거래 창과 보유 종목: 2행 -->
      <div class="bottom-section">
        <div class="trading-panel">
          <h3>주식 거래</h3>
          <select v-model="selectedStock" @change="updateStockUrl">
            <option v-for="stock in Object.keys(stockData)" :key="stock" :value="stock">{{ stock }}</option>
          </select>
          <p>
            현재가: ₩
            <span>
              {{ currentPrice }}
              <span v-if="beforePrice > 0" class="positive">▲ {{ beforePrice }}</span>
              <span v-if="beforePrice === 0">---</span>
              <span v-if="beforePrice < 0" class="negative">▼ {{ -beforePrice }}</span>
            </span>
          </p>
          <p v-if="currentDay < 11">최대 매수 가능 수량: {{ maxBuyableShares }}</p>
          <p v-if="currentDay < 11">최대 매도 가능 수량: {{ maxSellableShares || 0 }}</p>
          <input type="number" v-model.number="tradeVolume" @input="validateInput" placeholder="수량 입력" />
          <div class="button-group2">
            <button @click="executeTrade('buy')" class="buy-btn">매수(BUY)</button>
            <button @click="executeTrade('sell')" class="sell-btn">매도(SELL)</button>
          </div>
        </div>
        <div class="portfolio">
          <h3>보유 종목</h3>
          <table class="table">
            <thead>
              <tr>
                <th class="wide-column">종목</th>
                <th>전날 대비</th>
                <th class="narrow-column">보유량</th>
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
                  <td>
                    <span v-if="keyBeforePrice[key] > 0" class="positive">▲{{ keyBeforePrice[key] }}</span>
                    <span v-if="keyBeforePrice[key] === 0">--</span>
                    <span v-if="keyBeforePrice[key] < 0" class="negative">▼{{ -keyBeforePrice[key] }}</span>
                  </td>
                  <td>{{ totalQuantity[key] }}</td>
                  <td>{{ purchasePrice[key].toFixed(0) }}</td>
                  <td>{{ evaluationPrice[key].toFixed(0) }}</td>
                  <td :class="{ positive: evaluationProfit[key] > 0, negative: evaluationProfit[key] < 0 }">
                    {{ evaluationProfit[key].toFixed(0) }}
                  </td>
                  <td :class="{ positive: earningRate[key] > 0, negative: earningRate[key] < 0 }">
                    {{ earningRate[key].toFixed(2) }}
                  </td>
                </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
    </section>
  </div>
</template>


<script setup>
/* --------------------------- Imports --------------------------- */
import { ref, computed, onMounted } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import { useRouter, RouterView } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';
import Navbar from '@/components/Navbar.vue';
import Modal from "@/components/Modal.vue";
import ExchangeRateAlert from "@/components/ExchangeRateAlert.vue";

/* --------------------------- State --------------------------- */
const stockStore = useStockStore();
const router = useRouter();


// 상태 관리 변수
const currentDay = ref(1);  // 현재 날짜 (1~10일)
const seedMoney = 10000000  // 초기 자본금 (₩100,000,000), 상수로 두어 변경 불가능
const cash = ref(10000000); // 초기 현금 (₩100,000,000)
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

const tradePattern = ref({
  totalTrades: 0,          // 총 거래 횟수
  buyCount: 0,             // 매수 횟수
  sellCount: 0,            // 매도 횟수
  holdingPeriod: [],       // 평균 보유 기간
  riskLevel: 0,            // 위험 선호도
  sectorPreference: {},    // 선호 업종
  reactionToNews: 0        // 뉴스 반응도 // 이건 긍정적, 부정적 뉴스 키워드 반응 // 안쓰고있지만! 추후🙄
});

const investorType = ref('');  // 투자자 유형

/* --------------------------- Computed Values --------------------------- */

// 포트폴리오 가치 계산: (현재 주가 * 보유 수량)
const portfolioValue = computed(() => {
  return Object.keys(portfolio.value).reduce((total, stock) => {
    const totalQuantity = portfolio.value[stock].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0); // totalQuantity는 총 보유 수량
    if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
      const currentPrice = stockData.value[stock][9]?.close_price || 0;
      return total + (currentPrice * totalQuantity);
    } else {  // 10일차 이전에는 시가로 계산
      const currentPrice = stockData.value[stock]?.[currentDay.value - 1]?.open_price || 0;
      return total + (currentPrice * totalQuantity);
    }
  }, 0);
});

// 최대 매수 가능 수량 계산: (현금 / 현재 주가)
const maxBuyableShares = computed(() => (currentPrice.value > 0 ? Math.floor(cash.value / currentPrice.value) : 0));

const maxSellableShares = computed(() => {
  const totalQuantity = portfolio.value[selectedStock.value]?.transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
  return totalQuantity;
});

// 총 자산 = 현금 + 포트폴리오 가치
const totalValue = computed(() => {
  return cash.value + portfolioValue.value;
});

// 선택된 주식의 현재 가격
const currentPrice = computed(() => {
  if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
    return stockData.value[selectedStock.value][9]?.close_price || 0;
  } else {  // 10일차 이전에는 시가로 계산
    return stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price || 0;
  }
});

// 전일 대비 주가 변화
const beforePrice = computed(() => {
  if (currentDay.value === 1) {
    return 0;
  } else if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
  return stockData.value[selectedStock.value][9]?.close_price - stockData.value[selectedStock.value][9]?.open_price;
  } else {  // 10일차 이전에는 시가로 계산
    return stockData.value[selectedStock.value]?.[currentDay.value - 1]?.open_price - stockData.value[selectedStock.value][currentDay.value - 2]?.open_price;
  }
});

// 보유한 주식의 전일 대비 주가 변화
const keyBeforePrice = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    if (currentDay.value === 1) {
      result[key] = 0;
    } else if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
      result[key] = stockData.value[key][9]?.close_price - stockData.value[key][9]?.open_price;
    } else {  // 10일차 이전에는 시가로 계산
      result[key] = stockData.value[key]?.[currentDay.value - 1]?.open_price - stockData.value[key][currentDay.value - 2]?.open_price;
    }
  }
  return result
});

// 전체 수익률 = ((총 자산 / 시드 머니) - 1) * 100
const totalEarningRate = computed(() => {
  console.log('totalValue.value는 이렇게 출력됩니다.', totalValue.value);
  console.log('seedMoney는 이렇게 출력됩니다.', seedMoney);
  return ((totalValue.value / seedMoney) - 1) * 100;
});

// 평가 손익 = 평가 금액 - 총 매입 금액 (FIFO 방식 적용)
const totalEvaluationProfit = computed(() => {
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

// 해당 주식의 총 수량 계산
const totalQuantity = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    result[key] = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
  }
  return result
});

// 매입 단가 계산 = 총 매입 금액 / 보유 수량
const purchasePrice = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    const transactions = portfolio.value[key].transactions;  // 해당 종목의 거래 내역
    let remainingQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량
    let totalPurchaseAmount = 0;  // 총 매입 금액

    // FIFO 방식으로 매입 금액 계산
    for (let i = 0; i < transactions.length; i++) {  // 거래 내역을 순회하며
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

// 평가 금액 계산 = 현재 가격 * 보유 수량
const evaluationPrice = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);  // 보유 수량
    if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = selectedQuantity * selectedPrice
    } else {  // 10일차 이전에는 시가로 계산
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = selectedQuantity * selectedPrice
    }
    console.log('evaluationPrice의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})

// 평가 손익 계산 = 평가 금액 - 총 매입 금액
const evaluationProfit = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    // 보유 수량
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
    // 총 매입 금액
    const selectedTransaction = portfolio.value[key].transactions.reduce((totalTransaction, transaction) => totalTransaction + (transaction.quantity * transaction.price), 0);
    if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = selectedQuantity * selectedPrice - selectedTransaction
    } else {  // 10일차 이전에는 시가로 계산
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = selectedQuantity * selectedPrice - selectedTransaction
    }
    console.log('evaluationProfit의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})

// 수익률 계산 = 평가 금액 / 총 거래 금액 - 1
const earningRate = computed(() => {
  const result = {}
  for (const key in portfolio.value) {
    // 보유 수량
    const selectedQuantity = portfolio.value[key].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
    // 총 매입 금액
    const selectedTransaction = portfolio.value[key].transactions.reduce((totalTransaction, transaction) => totalTransaction + (transaction.quantity * transaction.price), 0);
    if (currentDay.value > 10) {  // 10일차 이후에는 종가로 계산
      const selectedPrice = stockData.value[key]?.[9]?.close_price
      result[key] = (selectedQuantity * selectedPrice) / selectedTransaction - 1  // 수익률 계산
    } else {  // 10일차 이전에는 시가로 계산
      const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
      result[key] = (selectedQuantity * selectedPrice) / selectedTransaction - 1  // 수익률 계산
    }
    console.log('earningRate의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})


// (4) 섹터 다양성 계산
const sectorDiversity = computed(() => {
  const sectorCounts = Object.values(tradePattern.value.sectorPreference); // 섹터별 투자 횟수
  const totalSectors = sectorCounts.reduce((a, b) => a + b, 0); // 총 투자 횟수
  const maxSectorPercentage = Math.max(...sectorCounts) / totalSectors; // 가장 큰 섹터 비중
  return 1 - maxSectorPercentage; // 섹터 다양성이 높을수록 값이 커짐
});

// (5) 종목 분산도 계산
const stockDiversity = computed(() => {
  const totalInvestedStocks = Object.keys(portfolio.value).length; // 현재 투자한 종목 수
  const maxStocks = Object.keys(stockStore.stockSectors).length;   // 전체 투자 가능한 종목 수
  // 종목 분산도 계산 (투자 종목 수 / 전체 종목 수)
  console.log("totalInvestedStocks,maxStocks",totalInvestedStocks,maxStocks)
  return totalInvestedStocks / maxStocks; // 분산도가 높을수록 값이 커짐
});


// 💥💥위험 선호도 계산💥💥
const calculateRiskLevel = computed(() => {
  const { buyCount, sellCount, holdingPeriod } = tradePattern.value;
  
  // 거래 빈도 계산 (0 ~ 1 사이로 정규화)
  const maxDailyTrades = 10; // 하루 최대 10회 거래로 가정
  const tradingFrequency = Math.min((buyCount + sellCount) / (currentDay.value * maxDailyTrades), 1)  // 0~1 사이 값

  // 2. 평균 보유 기간 계산
  const maxHoldingDays = 10; // 최대 보유 기간 10일로 가정
  const avgHoldingPeriod = holdingPeriod.length > 0 
    ? holdingPeriod.reduce((a, b) => a + b, 0) / holdingPeriod.length   // 보유 기록이 있으면 평균 계산
    : maxHoldingDays; // 보유 기록이 없으면 최대 보유 기간으로 설정
  const normalizedHoldingPeriod = Math.min(1 - (avgHoldingPeriod / maxHoldingDays), 1); // 0~1 사이 값

  // 3. 자산 분배율 계산
  const assetAllocation = portfolioValue.value / totalValue.value; // 투자 자산 / 총 자산

  // 4. 섹터 다양성 1 - (1 - 가장 큰 섹터 비율) = 다양할수록 전체 값 작아짐
  const sectorDiversityValue = 1 - sectorDiversity.value;
  
  // 5. 종목 분산도 (1 - 투자 종목 수 / 전체 종목 수) = 분산도 높을수록 전체 값 작아짐
  const diversity = 1 - stockDiversity.value;

  console.log( tradingFrequency * 0.3 , normalizedHoldingPeriod * 0.3 , assetAllocation * 0.2, sectorDiversityValue * 0.1, diversity * 0.1 );
  /* 1일차 30주만 샀으면                                                          
                    0.3                             0                       0.0716                     0.1                   0.0975
  */

  
  const riskLevel = (
    tradingFrequency * 0.3 +           // 거래 빈도: 30% 비중
    normalizedHoldingPeriod * 0.3 +    // 보유 기간: 30% 비중
    assetAllocation * 0.2 +            // 자산 분배율: 20% 비중
    sectorDiversityValue * 0.1 +       // 섹터 다양성: 10% 비중
    diversity * 0.1                    // 종목 분산도: 10% 비중
  );

  return riskLevel; // 0 ~ 1 사이 값
});


const startDateValue = computed(() => startDate.value || 'unknown');  // 시작 날짜
const endDateValue = computed(() =>
  stockData.value[selectedStock.value]?.[9]?.date || 'unknown'  // 종료 날짜
);

/* --------------------------- Functions --------------------------- */

// 랜덤한 시작 날짜 생성
async function fetchRandomDate() {
  try {
    // 랜덤한 날짜 생성 API 호출 backend/stocks/views.py generate_random_date
    const response = await axios.get('http://127.0.0.1:8000/api/stocks/generate_random_date/');
    if (response.data.status === 'success') {
      startDate.value = response.data.start_date;
      await updateStockUrl()  // 시작 날짜에 따른 주식 데이터 업데이트
    } else {
      console.error('Error generating random date:', response.data.message);
    }
  } catch (error) {
    console.error('Error generating random date:', error);
  }
}

// 주식 데이터 업데이트
async function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];
  if (stockCode) {
    // 주식 데이터 API 호출 backend/stocks/views.py find_stock_data
    const apiUrl = `http://127.0.0.1:8000/api/stocks/find_stock_data/${stockCode}/?start_date=${startDate.value}`;
    console.log("apiUrl : ",apiUrl)

    fetchStockData(apiUrl);
  }
}

// 주식 데이터 가져오기
async function fetchStockData(apiUrl) {
  try {
    const response = await axios.get(apiUrl);
    if (response.data.status === 'success') {
      // API로부터 받은 데이터를 저장
      stockData.value[selectedStock.value] = response.data.data.map(item => ({  
        date: item.date,  // 날짜
        open_price: item.open_price,  // 시가
        close_price: item.close_price,  // 종가
      }));
      console.log('stockData는 이렇게 출력됩니다.', stockData.value);
      updateChart();  // 차트 업데이트
    } else {
      console.error('Error fetching stock data:', response.data.message);
    }
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
}

// 뉴스 업데이트
async function updateNews() {
  const currentDate = ref(startDate.value);
  console .log('currentDate는 이렇게 출력됩니다.111', currentDate.value);
  if (startDate.value != stockData.value['삼성에스디에스']?.[currentDay.value - 1]?.date) {  // 시작 날짜가 주식 데이터의 날짜와 다를 경우
    currentDate.value = stockData.value['삼성에스디에스']?.[currentDay.value - 1]?.date  // 주식 데이터의 날짜로 업데이트
    console .log('currentDate는 이렇게 출력됩니다.222', currentDate.value);
  }
  try {
    // 뉴스 데이터 API 호출 backend/stocks/views.py fetch_news
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

// 차트 초기화
let chart;
function initializeChart() {
  const ctx = document.getElementById('chart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',  // 차트 종류: 선 그래프
    data: {
      labels: Array.from({ length: 11 }, (_, i) => (i === 10 ? '최종 결과' : `Day ${i + 1}`)), // X축: Day 1 ~ 10
      datasets: [{
        label: 'Stock Price',  // 라벨
        data: stockData.value[selectedStock.value].slice(0, currentDay.value), // 주가 데이터
        borderColor: 'rgba(75, 192, 192, 1)',  // 선 색상
        borderWidth: 1  // 선 두께
      }]
    },
    options: { scales: { y: { beginAtZero: false } } },  // Y축 0부터 시작하지 않도록 설정
  });
}

// 차트 업데이트
function updateChart() {
  const data = stockData.value[selectedStock.value].map(item => item.open_price).slice(0, currentDay.value);  // 주가 데이터
  if (currentDay.value >= 10) {  // 10일차 이후에는 종가로 업데이트
    data[currentDay.value - 1] = stockData.value[selectedStock.value][currentDay.value - 2].close_price;
  }
  chart.data.datasets[0].data = data; // 차트에 데이터 반영
  chart.update(); // 차트 업데이트
}




// Next Day 다음 날짜로 진행
async function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;  // 다음 날짜로 업데이트
    updateChart(); // 차트 업데이트
    updateNews();  // 뉴스 업데이트
  } else {
    // 게임 종료 및 최종 자산 계산
    currentDay.value++; // 마지막 날짜까지 진행
    updateChart(); // 차트 업데이트
    console.log('stockData는 이렇게 출력됩니다.', stockData.value);

    const finalPortfolioValue = Object.keys(portfolio.value).reduce((total, stock) => {  // 최종 포트폴리오 가치 계산
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
    Object.keys(portfolio.value).forEach((stock) => {  // 보유한 주식 종목별로 반복
      const transactions = portfolio.value[stock].transactions;  // 해당 종목의 거래 내역
      transactions.forEach((transaction) => {  // 거래 내역을 순회하며
        const holdingDays = 10 - transaction.day; // 마지막 날(10일) 기준 보유 기간 계산
        tradePattern.value.holdingPeriod.push(holdingDays); // 보유 기간 기록
      });
    });
    console.log('Updated holdingPeriod:', tradePattern.value.holdingPeriod);

    const riskLevel = calculateRiskLevel.value;  // 위험 선호도 계산

    if (riskLevel < 0.3) investorType.value = '안정 추구형'; /* 아무것도 안하면 -INF : 안정 추구형이 나오도록 했음  */
    else if (riskLevel < 0.6) investorType.value = '균형 투자형';
    else if (riskLevel < 0.8) investorType.value = '공격 투자형';
    else investorType.value = '투기형';

    // 최종 자산과 투자자 유형 서버로 전송 (토큰 포함) backend/accounts/views.py update_max_score
    const response = await fetch('http://127.0.0.1:8000/accounts/update_max_score/', {
      method: 'POST',
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`, // 토큰을 헤더에 포함
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ max_score: finalTotalValue.value, my_investor_type: investorType.value }) // 최종 자산을 서버로 전송
    });

    // 게임 종료 메시지 출력
    alert(`게임 종료!\n최종 자산: ₩${finalTotalValue.value}\n투자자 유형: ${investorType.value}\n주식 데이터 기간: ${startDateValue.value} ~ ${endDateValue.value}`);
    if (response.ok) {
      console.log('Game over. Your total value is ₩', finalTotalValue.value); 
    } else {
      console.error('Failed to update max score:', response.statusText);
    }
  }
}

// 새로고침 없이 게임 초기화
function restartGame() {
 location.reload();  // 새로고침
}

function goToExchangeRateCalculator() {
  router.push('/exchange-rate-alert');  // finances 페이지로 이동
}

function goToLeaderboard() {
  router.push('/leaderboard'); // ExchangeRateAlert 페이지로 이동
}

/* --------------------------- Lifecycle --------------------------- */
onMounted(async () => {  // 페이지 로딩 시 실행
  await fetchRandomDate();  // 랜덤한 시작 날짜 생성
  updateStockUrl();  // 주식 데이터 업데이트
  initializeChart();  // 차트 초기화
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

  if (type === 'buy') {  // 매수
    // 매수 조건: 현금이 충분하고, 거래량이 0보다 큼
    if (volume > 0 && cash.value >= price * volume) {
      cash.value -= price * volume; // 현금 감소

      // 매수 거래 내역 추가 (FIFO 방식 적용을 위해 배열에 추가)
      portfolio.value[selectedStock.value].transactions.push({
        quantity: volume,  // 거래량 추가
        price: price,  // 거래 가격 추가
        day: currentDay.value  // 거래 시점 추가
      });
      
      console.log(`매수 완료: ${volume}주, 가격: ${price}`);

      tradePattern.value.buyCount += volume;  // 매수 거래 횟수 업데이트
      tradePattern.value.totalTrades += volume;  // 총 거래 횟수 업데이트
      // 업종 선호도 기록
      const sector = stockStore.stockSectors[selectedStock.value];
      tradePattern.value.sectorPreference[sector] = (tradePattern.value.sectorPreference[sector] || 0) + 1;

      console.log("transactions 확인하기 : ", portfolio.value[selectedStock.value].transactions);

    } else {
      alert('Not enough cash or invalid quantity for buying.'); // 에러 메시지
    }
  } else if (type === 'sell') {
    // 보유 주식 수량 계산
    const totalQuantityAvailable = portfolio.value[selectedStock.value].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0);
    
    // 매도 조건: 보유 주식이 충분하고, 거래량이 0보다 큼
  if (volume > 0 && totalQuantityAvailable >= volume) {
    let remainingQuantity = volume;  // 매도할 수량
    let totalCost = 0;  // 총 매도 금액

    // FIFO 방식으로 매도
    while (remainingQuantity > 0) {  // 매도할 수량이 남아있는 동안 반복
      const firstTransaction = portfolio.value[selectedStock.value].transactions[0]; // 가장 오래된 거래 내역

      if (!firstTransaction) {  // 거래 내역이 없으면 에러 메시지 출력
        console.error('Error: No transaction found in portfolio for sell operation.');
        break;
      }

      // 보유 기간 계산 및 기록
      const holdingDays = currentDay.value - firstTransaction.day;
      tradePattern.value.holdingPeriod.push(holdingDays);

      // 매도 수량이 해당 거래 내역의 수량보다 작거나 같으면 해당 거래 내역을 모두 소진
      if (firstTransaction.quantity <= remainingQuantity) {
        totalCost += firstTransaction.quantity * firstTransaction.price;  // 총 매도 금액 계산
        remainingQuantity -= firstTransaction.quantity;  // 남은 수량 업데이트
        portfolio.value[selectedStock.value].transactions.shift(); // 해당 거래 내역 제거
      } else {  // 매도 수량이 해당 거래 내역의 수량보다 크면 일부만 소진
        totalCost += remainingQuantity * firstTransaction.price;  // 총 매도 금액 계산
        firstTransaction.quantity -= remainingQuantity;  // 해당 거래 내역의 수량 업데이트
        remainingQuantity = 0;  // 남은 수량 초기화
      }
      console.log("transactions 확인하기 : ", portfolio.value[selectedStock.value].transactions);

    }

    // 매도 완료 후 현금 증가
    cash.value += price * volume; // 현금 증가

    console.log(`매도 완료: ${volume}주, 가격: ${price}, 총 매도 금액: ${totalCost}`);

    // 매도 거래 횟수 업데이트
    tradePattern.value.sellCount += volume;
    tradePattern.value.totalTrades += volume;

  } else {
    alert('Not enough shares to sell.');
  }
}

// 위험 선호도 계산
console.log("Calculating risk level...");
try {
  const riskLevel = calculateRiskLevel.value;  // 위험 선호도 계산
  tradePattern.value.riskLevel = riskLevel;
  console.log("Risk Level: ", riskLevel);
} catch (error) {
  console.error("Error accessing calculateRiskLevel: ", error);
}


// 거래 완료 후 입력값 초기화
tradeVolume.value = 0;

 
console.log('tradePattern@@@@@@@@@@@@@@', tradePattern.value);
} // executeTrade 함수 끝


// 모달 관련 시작 -----------------
// 상태 관리
const isModalOpen = ref(false);

// 모달 열기
const openModal = () => {
  isModalOpen.value = true;
};

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false;
};
// 모달 관련 끝 -----------------


</script>

<style scoped>
/* 전체 레이아웃 */
.game-container {
  display: flex;
  height: 100vh;
  background-color: #f4f9ff;
  color: #333;
  overflow: hidden;
}

/* 뉴스와 차트를 나란히 배치 */
.top-section {
  display: flex;
  gap: 20px;
  /* margin-bottom: 20px; */
}

/* 주식 거래 창과 보유 종목 창을 나란히 배치 */
.bottom-section {
  display: flex;
  gap: 20px;
}


/* 사이드바 */
.sidebar {
  width: 25%;
  background-color: #004aad;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px; /* 요소 간 일정한 간격 */
  color: white;
  box-sizing: border-box;
  overflow-y: auto;
}
.sidebar h6 {
  font-size: 1rem; /* 적절한 크기 */
  font-weight: 400; /* 중간 정도의 두께 */
  color: #d4ebf8; /* 사이드바와 어울리는 밝은 텍스트 색 */
  text-align: center; /* 텍스트 가운데 정렬 */
  margin-bottom: 15px; /* 아래 간격 추가 */
  line-height: 1.5; /* 텍스트 간격 조정 */
}

.game-title {
  font-size: 2rem; /* 통일된 글자 크기 */
  font-weight: bold;
  text-align: center;
  /* margin-bottom: 20px; */
}

/* Day Counter */
.dayyy {
  font-size: 1.4rem;
  font-weight: 600;
  text-align: center;
}








.progress-bar {
  width: 80%; /* 막대 길이 조정 */
  height: 10px;
  background-color: #e0e0e0;
  border-radius: 5px;
  margin-top: 3px; /* Day 텍스트와 막대 사이 간격 */
  overflow: hidden;
}

.progress {
  height: 100%;
  background-color: #E38E49;
  transition: width 0.3s ease;
  border-radius: 6px;
}

.next-day-btn {
  align-self: center;
  background-color: #e38e49;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.next-day-btn:hover {
  background-color: #ffb172;
  color: white;
}

/* Portfolio Overview */
.portfolio-overview {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  margin: 10px 0;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.portfolio-overview th,
.portfolio-overview td {
  padding: 12px;
  border: 1px solid #ddd;
}

.portfolio-overview th {
  background-color: #bcd9ff;
  color: black;
}

.portfolio-overview td {
  font-size: 1rem;
}

/* 환율계산기 , 랭킹보기 버튼 그룹 */
.button-group {
  display: flex;
  flex-direction: row; /* 버튼을 가로로 배치 */
  gap: 15px; /* 버튼 간 간격 */
  justify-content: center; /* 버튼을 가운데 정렬 */
}

.button-group .btn {
  padding: 10px 20px;
  background-color: #397edb;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.button-group .btn:hover {
  background-color: #d4ebf8;
  color: #004aad;
}


/* 공통 컨테이너 스타일 */
.day-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 150px; /* 동일한 높이 설정 */
  margin-bottom: 20px; /* 다른 섹션과의 간격 */
  background-color: #004aad; /* 사이드바와 동일한 배경색 */
  border-radius: 10px; /* 부드러운 모서리 */
  padding: 10px; /* 내부 여백 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
}

/* Day 진행률 섹션 */
.progress-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}



/* 최종 결과 섹션 */
.final-results {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%; /* 동일한 높이 적용 */
  color: white;
  font-size: 0.9rem;
}

.final-results .result-item {
  margin: 5px 0;
}

.result-buttons {
  font-size: 0.5rem;
  display: flex;
  gap: 10px; /* 버튼 간 간격 */
  margin-top: 15px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  font-size: 0.9rem;
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}



/* 여기까지 왼쪽부분 ---------------------------------------------------------------*/




/* 기타 공통 버튼 등*/
.btn {
  padding: 10px 20px;
  background-color: #397edb;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  background-color: #D4EBF8;
}

.positive {
  color: red;
}

.negative {
  color: blue;
}





/* 메인 콘텐츠 */
.main-content {
  font-size: 0.9rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  background-color: #ffffff;
  box-sizing: border-box;
  overflow-y: auto;
}

.news-section {
  font-size: 0.9rem;
  flex : 1;
  width: 100%;
  background-color: #fefefe;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.charts-section {
  flex : 1;
  background-color: #f0f4ff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 이하 거래 및 보유 종목 ---------------------------------------------------*/

/* 공통 섹션 스타일 */
.trade-and-holdings {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;
  align-items: flex-start; /* 위쪽 정렬 */
}

/* 개별 섹션 스타일 */
.trading-panel{
  /* flex: 1; */
  background-color: #f9fbff; /* 부드러운 흰색 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow: hidden; /* 내용이 넘치지 않도록 */
  height: 330px; /* 최소 높이를 설정하여 항상 일정 크기 유지 */
}

/* 주식거래,보유종목 타이틀 스타일 */
.news-section h3,
.trading-panel h3,
.charts-section h3,
.portfolio h3 {
  font-size: 1.2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 15px;
}

/* 주식 거래 섹션 */
.trading-panel select {
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  border: 1px solid #d0d7e6;
  border-radius: 5px;
  font-size: 1rem;
}

.trading-panel p {
  font-size: 0.9rem;
  color: #333;
  margin: 5px 0;
}

.trading-panel input {
  width: 100%;
  padding: 10px;
  border: 1px solid #d0d7e6;
  border-radius: 5px;
  font-size: 1rem;
  margin-bottom: 10px;
}

/* 매수/매도 버튼 */
/* 버튼 그룹 스타일 */
.trading-panel .button-group2 {
  display: flex; /* flexbox로 배치 */
  justify-content: space-between; /* 버튼들을 양쪽에 균등 배치 */
  gap: 10px; /* 버튼 간의 간격 */
  /* width: 100%; 부모 요소에 맞춰 확장 */
}

/* 매수/매도 버튼 */
.trading-panel .buy-btn,
.trading-panel .sell-btn {
  flex: 1; /* 버튼의 크기를 균등 분배 */
  width: 150px; /* 버튼 너비 */
  height: 50px; /* 버튼 높이 */
  padding: 10px 15px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center; /* 버튼 내 텍스트 정렬 */
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

.trading-panel .buy-btn {
  background-color: #e38e49;
  color: white;
}

.trading-panel .buy-btn:hover {
  background-color: #ffb172;
}

.trading-panel .sell-btn {
  background-color: #e38e49;
  color: white;
}

.trading-panel .sell-btn:hover {
  background-color: #ffb172;
}



/* 보유 종목 섹션 */
.portfolio {
  flex: 1; /* 균등 분배 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* 시작 위치로 정렬 */
  background-color: #f9fbff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-height: 330px; /* 최소 높이 */
}

/* 보유 종목 테이블 스타일 */
.portfolio table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  font-size: 0.9rem;
  margin-top: 15px; /* 제목과의 간격 */
  table-layout: fixed; /* 각 셀의 너비를 균등하게 */
}

.portfolio th,
.portfolio td {
  padding: 10px;
  border: 1px solid #d0d7e6;
  font-size: 0.9rem;
}

.portfolio th {
  background-color: #f0f4ff;
  font-weight: bold;
}

.portfolio th.wide-column,
.portfolio td.wide-column {
  width: 20%; /* 종목 열 너비 */
}

.portfolio th.narrow-column,
.portfolio td.narrow-column {
  width: 10%; /* 보유량 열 너비 */
}

/* 데이터가 없을 때 */
.portfolio .no-data {
  text-align: center;
  padding: 20px;
  font-size: 1rem;
  color: #999; /* 회색 텍스트 */
}

.portfolio .positive {
  color: red; /* 상승 표시 */
}

.portfolio .negative {
  color: blue; /* 하락 표시 */
}



/* -------------------------------------------- */



</style>