<template>
  <div>
    <h2>환율 알림 설정</h2>
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
import { ref } from 'vue';

export default {
  setup() {
    const currency = ref('USD'); // 기본 통화는 USD로 설정
    const targetRate = ref(null);
    const exchangeRate = ref(null);
    const alertSet = ref(false);
    const showAlert = ref(false);

    // 목표 환율 설정 함수
    const setAlert = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/accounts/set_alert/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            currency: currency.value,
            target_rate: targetRate.value,
          }),
        });
        const data = await response.json();
        if (response.ok && data.status === 'success') {
          alertSet.value = true;
          alert("목표 환율이 설정되었습니다.");
          console.log("알림 설정 성공:", data);
        } else {
          console.error("알림 설정 실패:", data);
        }
      } catch (error) {
        console.error("목표 환율 설정 중 오류가 발생했습니다.", error);
      }
    };

    // 현재 환율 정보 및 알림 확인 함수
    const fetchExchangeRate = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/accounts/check_exchange_rate/");
        const data = await response.json();
        console.log("API 응답 데이터:", data); // 추가된 디버깅 로그
        if (response.ok) {
          if (data.current_rate !== undefined) {
            exchangeRate.value = data.current_rate;
            showAlert.value = data.alert;
            console.log("현재 환율:", exchangeRate.value); // 디버그용 로그 추가
            console.log("목표 환율 이하로 내려갔는가?", showAlert.value); // 디버그용 로그 추가
          } else {
            console.error("환율 데이터가 없습니다:", data);
            exchangeRate.value = null;
          }
        } else {
          console.error("환율 정보 가져오기 실패:", data);
          exchangeRate.value = null;
        }
      } catch (error) {
        console.error("환율 정보 가져오기 중 오류가 발생했습니다.", error);
        exchangeRate.value = null;
      }
    };

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

    return {
      currency,
      targetRate,
      exchangeRate,
      alertSet,
      showAlert,
      setAlert,
      fetchExchangeRate,
    };
  },
};
</script>

<style scoped>
.alert {
  color: red;
  font-weight: bold;
}
</style>