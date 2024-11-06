<template>
  <div>
    <h2>현재 환율 정보</h2>
    <button @click="fetchExchangeRate">환율 가져오기</button>
    <div v-if="exchangeRate !== null">
      <p>USD 기준 환율 (KRW): {{ exchangeRate }}</p>
    </div>
    <div v-else>
      <p>환율 정보를 불러올 수 없습니다. 다시 시도해 주세요.</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      exchangeRate: null,
    };
  },
  methods: {
    async fetchExchangeRate() {
      try {
        const response = await fetch("http://127.0.0.1:8000/accounts/get_exchange_rate/");
        const data = await response.json();
        console.log("받은 데이터:", data);  // 데이터 구조 확인용

        // data 배열에서 cur_unit이 "USD"인 객체 찾기 (USD 기준 환율을 찾음)
        const usdData = data.find(item => item.cur_unit === "USD");

        if (usdData && usdData.deal_bas_r) {
          this.exchangeRate = usdData.deal_bas_r;  // deal_bas_r 값이 USD의 기준 환율로 설정
        } else {
          this.exchangeRate = "USD 데이터 없음";
        }
      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류가 발생했습니다.", error);
        this.exchangeRate = "오류 발생";
      }
    },
  },
};
</script>
