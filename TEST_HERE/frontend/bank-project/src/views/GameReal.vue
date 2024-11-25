<template>
  <div>
    <!-- Header Section -->
    <div class="header">
      <div class="container">
        <h1>10-Day Stock Investment Game</h1>
      </div>
    </div>
  

    <!-- News Section -->
    <div class="news-container" v-if="currentDay < 11"> <!--10일차까지만 표시되어야함-->
      
      <h3>Latest News</h3>
      <ul>
        <!-- 주식 관련 최신 뉴스 제목을 최대 10개 출력 -->
        <li v-for="(title, index) in newsTitles" :key="index">
          {{ title }}
        </li>
        <!-- 뉴스 데이터가 로드되지 않았을 때 출력 -->
        <h5 v-if="newsTitles.length === 0">해당 날짜의 뉴스를 로딩 중입니다.</h5>
      </ul>
      
      <!-- ExchangeRateAlert로 이동하는 버튼 -->
      <button @click="goToExchangeRateAlert" class="btn btn-primary" style="margin-top: 10px;"> 환율 알림 기능 </button>

    </div>


    <!-- Game UI Section -->
    <div class="container">
      <!-- 현재 날짜를 표시하는 섹션 -->
      <div class="day-counter"  v-if="currentDay < 11"> Day <span>{{ currentDay }}</span> / 10 </div> <!-- 10일차까지 표시 -->
      <div class="day-counter"  v-if="currentDay > 10"> Day <span>10</span> / 10 <!-- 게임 종료 후 결과 표시 -->
        <div>최종 자산: {{finalTotalValue}} </div>
        <div>투자자 유형: {{investorType}} </div>
        <div>실제 주식 데이터 기간 : {{startDateValue}} ~ {{endDateValue}}</div>
        <button @click="goFinanceRecommend" class="btn btn-primary">당신에게 맞는 펀드 상품 추천 바로가기</button>
        <button @click="restartGame" class="btn btn-primary">Restart Game</button>
      </div>

      
      <div class="game-container">
        <!-- 전체 수익률, 평가 손익 등을 표시하는 표 -->
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
            <!-- 각 데이터에 따라 색상 변화 -->
            <td :class="{'color-red': totalEarningRate > 0, 'color-blue': totalEarningRate < 0}">{{ totalEarningRate.toFixed(2) }}%</td>
            <td :class="{'color-red': totalEvaluationProfit > 0, 'color-blue': totalEvaluationProfit < 0}">{{ totalEvaluationProfit }}</td>

            <td>{{ portfolioValue }}</td>
            <td>{{ seedMoney }}</td>
            <td>{{ cash }}</td>
            <td>{{ totalValue }}</td>
          </tr>
        </table>
        
        <!-- 차트 및 거래 패널 -->
        <div class="container">
          <div class="row">
            <div class="chart-section col-8">
              <canvas id="chart"></canvas> <!-- 주가 데이터를 표시하는 차트 -->
            </div>
            <div class="col-4">
              <div class="trading-panel"> <!-- 주식 거래 패널 -->
                <select v-model="selectedStock" @change="updateStockUrl"> <!-- 선택할 수 있는 주식 목록 -->
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
                  <!-- 선택한 주식 정보 -->
                  <div class="stock-info">
                    <h3>Current Price: ₩<span>{{ currentPrice }}</span></h3>

                    <!-- 전일 대비 주가 변화 -->
                    <h4 v-if="beforePrice > 0" class="color-red">▲ {{ beforePrice }}</h4>
                    <h4 v-if="beforePrice === 0">---</h4>
                    <h4 v-if="beforePrice < 0" class="color-blue">▼ {{ -beforePrice }}</h4>

                    <p v-if="currentDay < 11">Max Buyable Shares: {{ maxBuyableShares }}</p>  <!-- 최대 매수 가능 수량 -->
                  </div>

                  <!-- 매수/매도량 입력 -->
                  <input 
                    type="number" 
                    v-model.number="tradeVolume" 
                    @input="validateInput"
                    placeholder="Enter quantity"
                    v-if="currentDay < 11"
                  />

                  <!-- 매수/매도 거래 버튼 -->
                  <div class="trade-buttons" style="margin-top: 5px;"  v-if="currentDay < 11">
                    <button class="trade-button" @click="executeTrade('buy')" v-if="currentPrice !== 0">Buy</button>
                    <button class="trade-button" v-else>Buy</button>
                    <button class="trade-button" @click="executeTrade('sell')"v-if="currentPrice !== 0">Sell</button>
                    <button class="trade-button" v-else>Sell</button>
                    
                  </div>
                </div>

              </div><!--traing-panel 끝-->

              
              <div class="portfolio"> <!-- 보유 종목 표시 -->
                <br>
                <h3>Your Holdings</h3>
                <div>
                  <template v-for="key in Object.keys(portfolio)" :key="key">
                    <div v-if="totalQuantity[key] > 0">
                      {{ key }}: {{ totalQuantity[key] }} shares  <span v-if="keyBeforePrice[key] > 0" class="color-red">▲{{ keyBeforePrice[key] }}</span><span v-if="keyBeforePrice[key] === 0">--</span><span v-if="keyBeforePrice[key] < 0" class="color-blue">▼{{ -keyBeforePrice[key] }}</span>
                      <br>
                    </div>
                  </template>
                </div>
              </div><!-- portfolio 끝-->

              <!-- 다음 날로 이동 버튼 -->
              <button v-if="currentDay < 11 && currentPrice === 0">Next Day</button>
              <button @click="nextDay" v-else-if="currentDay < 11">Next Day</button>

            </div><!-- col-4 끝 -->
          </div><!-- row 끝-->
        </div><!-- container 끝 -->
      </div><!-- game-container 끝 -->
    </div><!--container 끝-->
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
import { ref, computed, onMounted } from 'vue';
import { useStockStore } from '@/stores/StockStore';
import { useRouter } from 'vue-router';
import axios from 'axios';
import Chart from 'chart.js/auto';

/* --------------------------- State --------------------------- */
const stockStore = useStockStore();
const router = useRouter();


// 상태 관리 변수
const currentDay = ref(1);  // 현재 날짜 (1~10일)
const seedMoney = 100000000  // 초기 자본금 (₩100,000,000), 상수로 두어 변경 불가능
const cash = ref(100000000); // 초기 현금 (₩100,000,000)
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
  currentDay.value = 1;  // 현재 날짜 초기화
  cash.value = 100000000;  // 초기 현금 (₩100,000,000)
  finalTotalValue.value = 0;  // 최종 자산 초기화
  portfolio.value = {};  // 보유 주식 초기화
  investorType = ""; // 투자자 유형 초기화
  alert("Game has been restarted!");  // 게임 재시작 메시지
  updateStockUrl();  // 주식 데이터 업데이트
  initializeChart();  // 차트 초기화
}

function goFinanceRecommend() {
  router.push('/finances');  // finances 페이지로 이동
}

function goToExchangeRateAlert() {
  router.push('/exchange-rate-alert'); // ExchangeRateAlert 페이지로 이동
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
</script>

<style scoped>

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