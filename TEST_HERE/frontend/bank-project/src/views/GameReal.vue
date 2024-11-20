<template>
  <div>
    <div class="header">
      <div class="container">
        <h1>10-Day Stock Investment Game</h1>
      </div>
    </div>

    <div class="container">
      <div class="day-counter"  v-if="currentDay < 11">Day <span>{{ currentDay }}</span> / 10</div>
      <div class="day-counter"  v-if="currentDay > 10">Day <span>10</span> / 10</div>

      
        <div class="game-container">
          <!-- <div class="balance-panel">
            <h3>Account Balance</h3>
            <div class="balance-info">Cash: ₩<span>{{ cash }}</span></div>
            <div class="balance-info">Portfolio Value: ₩<span>{{ portfolioValue }}</span></div>
            <div class="balance-info">Total Value: ₩<span>{{ totalValue }}</span></div>
            <h3 class="final-score" v-if="finalTotalValue !== 0">최종 금액은 {{ finalTotalValue }}원 입니다.</h3>
          </div> -->

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

                  <!-- 기존코드 - 음수 및 문자 입력 방지는 구현되어있음 -->
                  <!-- <div class="stock-info">
                    <br>
                    <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>
                    <br>
                  </div>                  
                  <input 
                    type="number" 
                    v-model.number="tradeVolume" 
                    @input="validateInput"
                    placeholder="Enter quantity"
                  />
                   -->
                  <!-- 시도 1 -->
                  <!-- <div>

                    <div class="stock-info">
                      <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>
                      <p>Max Buyable Shares: {{ maxBuyableShares }}</p>
                    </div>


                    <input 
                      type="number" 
                      v-model.number="tradeVolume" 
                      @input="validateInput"
                      :max="maxBuyableShares"
                      placeholder="Enter quantity"
                    />
                  </div> -->

                  <!-- 시도 2 -->
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
                      <button class="trade-button" @click="executeTrade('buy')">Buy</button>
                      <button class="trade-button" @click="executeTrade('sell')">Sell</button>
                    </div>
                  </div>

                  <!-- ---------------------------------------------------------- -->

                  <!-- <div class="trade-buttons">
                    <br>
                    <button class="trade-button" @click="executeTrade('buy')">Buy</button>
                    <button class="trade-button" @click="executeTrade('sell')">Sell</button>
                    <br>
                  </div> -->
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

              <button @click="nextDay"  v-if="currentDay < 11">Next Day</button>
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
        <tr v-if="portfolio[key].transactions != []">
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
import { ref, computed, onMounted, watch } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import axios from 'axios';
import Chart from 'chart.js/auto';
// import api from '@/api';

// 주식 데이터 저장소 사용
const stockStore = useStockStore();

// 상태 관리 변수
const currentDay = ref(1);  // 현재 날짜 (1~10일)
const seedMoney = 10000000
const cash = ref(10000000); // 초기 현금 (₩10,000,000)
const portfolio = ref({});  // 보유 주식 정보 (주식 이름: 수량)
const selectedStock = ref('삼성에스디에스');  // 선택된 주식
const tradeVolume = ref(0); // 거래량 (사용자 입력)
const startDate = ref(''); // 난수로 받을 시작 날짜
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

let chart; // 차트를 저장할 변수
const finalTotalValue = ref(0); // 게임 종료 후 최종 자산

// 계산된 값
const portfolioValue = computed(() => {
  // 포트폴리오의 총 가치를 계산 (보유 주식 * 현재 주가)
  console.log('portfolio.value는 이렇게 출력됩니다.', portfolio.value);

  return Object.keys(portfolio.value).reduce((total, stock) => {
    const totalQuantity = portfolio.value[stock].transactions.reduce((totalQuantity, transaction) => totalQuantity + transaction.quantity, 0); 

    const currentPrice = stockData.value[stock]?.[currentDay.value - 1]?.open_price || 0;

    // 포트폴리오 가치 계산: (현재 주가 * 보유 수량)
    return total + (currentPrice * totalQuantity); // totalQuantity는 총 보유 수량
  }, 0);
});

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
  return ((totalValue.value / cash.value) - 1) * 100;
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
    const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
    result[key] = selectedQuantity * selectedPrice
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
    const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
    result[key] = selectedQuantity * selectedPrice - selectedTransaction
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
    const selectedPrice = stockData.value[key]?.[currentDay.value - 1]?.open_price
    result[key] = (selectedQuantity * selectedPrice) / selectedTransaction - 1
    console.log('earningRate의 result[key]는 이렇게 출력됩니다.', result[key]);
  }
  return result
})

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

// 주식 데이터 업데이트 URL 설정
function updateStockUrl() {
  const stockCode = stockStore.stockMapping[selectedStock.value];  // 선택된 주식의 코드 가져오기
  if (stockCode) {
    const apiUrl = `http://127.0.0.1:8000/api/stocks/${stockCode}/?start_date=${startDate.value}`; // API URL 생성
    console.log('API URL:', apiUrl); 
    fetchStockData(apiUrl); // 주식 데이터 가져오기
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


// 다음 날짜로 진행
function nextDay() {
  if (currentDay.value < 10) {
    currentDay.value++;  // 날짜 증가
    updateChart(); // 차트 업데이트
  } else {
    // 게임 종료 및 최종 자산 계산
    currentDay.value++; // 마지막 날짜까지 진행
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
onMounted(async () => {
  await fetchRandomDate();
  updateStockUrl(); // 초기 데이터 가져오기
  // fetchStockData(); // API 호출
  initializeChart(); // 차트 초기화
  updateChart(); // 차트 업데이트
  // updateStockUrl();
  // initializeChart();
  // updateChart();
});

// onMounted(() => {
// });


// Watchers to update the UI when values change
// 값 변경 감지 및 업데이트
watch([cash, portfolio, currentDay, selectedStock], () => {
  updateChart(); // 상태 변경 시 차트 업데이트
});

///////////////////////////
// 계산된 값: 최대 매수 가능 수량
const maxBuyableShares = computed(() => {
  return currentPrice.value > 0 ? Math.floor(cash.value / currentPrice.value) : 0;
});

// 계산된 값: 최대 매도 가능 수량
const maxSellableShares = computed(() => {
  return portfolio.value[selectedStock.value] || 0; // 선택된 주식의 보유 수량 반환
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
        price: price
      });

      console.log(`매수 완료: ${volume}주, 가격: ${price}`);
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
      }

      // 매도 완료 후 현금 증가
      cash.value += price * volume; // 현금 증가

      console.log(`매도 완료: ${volume}주, 가격: ${price}, 총 매도 금액: ${totalCost}`);
    } else {
      alert('Not enough shares to sell.'); // 보유 주식 수량이 부족함을 알리는 메시지
    }
  }

  // 거래 완료 후 입력값 초기화
  tradeVolume.value = 0;
}


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