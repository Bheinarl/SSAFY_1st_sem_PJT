<!-- ExchangeRateAlert.vue -->

<template>
  <div>
    <h2>해외 소비를 위한 환율 알림 설정</h2>
    <form @submit.prevent="setAlert">
      <input v-model="currency" placeholder="통화(예: USD)" />
      <input v-model="targetRate" type="number" placeholder="목표 환율" />
      <button type="submit">알림 설정</button>
    </form>
    <p v-if="alertSet">환율 알림이 설정되었습니다!</p>

    <h2>현재 환율 정보</h2>
    <button @click="fetchExchangeRate">환율 가져오기</button>
    <div v-if="exchangeRate !== null">
      <p>{{ currency }} 기준 환율 (KRW): {{ exchangeRate }}</p>
      <p v-if="showAlert" class="alert">환율이 목표 이하로 내려갔습니다! 현재 환율: {{ exchangeRate }}</p>
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
      currency: 'USD', // 기본 통화는 USD로 설정
      targetRate: '',
      exchangeRate: null,
      alertSet: false,
      showAlert: false,
    };
  },
  methods: {
    async setAlert() {
      try {
        const response = await fetch("http://127.0.0.1:8000/accounts/set_alert/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            currency: this.currency,
            target_rate: this.targetRate,
          }),
        });
        const data = await response.json();
        if (data.status === 'success') {
          this.alertSet = true;
          alert("목표 환율이 설정되었습니다.");
        }
      } catch (error) {
        console.error("목표 환율 설정 중 오류가 발생했습니다.", error);
      }
    },
    async fetchExchangeRate() {
      try {
        // Django 백엔드에서 현재 환율과 알림 여부를 확인
        const response = await fetch("http://127.0.0.1:8000/accounts/check_exchange_rate/");
        const data = await response.json();
        
        // 현재 환율을 상태에 저장
        this.exchangeRate = data.current_rate;
        // 목표 환율 이하일 경우 showAlert를 true로 설정하여 알림 표시
        this.showAlert = data.alert;
        
        // 디버그용 로그 추가
        console.log("현재 환율:", this.exchangeRate);
        console.log("목표 환율 이하로 내려갔는가?", this.showAlert);

      } catch (error) {
        console.error("환율 데이터를 가져오는 중 오류가 발생했습니다.", error);
      }
    },

    // async fetchExchangeRate() {
    //   try {
    //     const response = await fetch("http://127.0.0.1:8000/accounts/check_exchange_rate/");
    //     const data = await response.json();
    //     this.exchangeRate = data.current_rate;
    //     this.showAlert = data.alert;
    //   } catch (error) {
    //     console.error("환율 데이터를 가져오는 중 오류가 발생했습니다.", error);
    //   }
    // },
  },
};
</script>

<style scoped>
.alert {
  color: red;
  font-weight: bold;
}
</style>
