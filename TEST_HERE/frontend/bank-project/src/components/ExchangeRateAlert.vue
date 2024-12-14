<template>
  <!-- <header> <Navbar /> </header> -->
  <div class="exchange-container">
    <h2 class="title">환율 알림 설정</h2>
    <form @submit.prevent="setAlert" class="alert-form">
      <select v-model="currency" class="select">
        <option value="" disabled>환율을 알아볼 외화를 선택하세요</option>
        <option value="CAD">CAD - 캐나다 달러</option>
        <option value="AED">AED - 아랍에미리트 디르함</option>
        <option value="AUD">AUD - 호주 달러</option>
        <option value="BHD">BHD - 바레인 디나르</option>
        <option value="BND">BND - 브루나이 달러</option>
        <option value="CHF">CHF - 스위스 프랑</option>
        <option value="CNH">CNH - 중국 위안화</option>
        <option value="DKK">DKK - 덴마크 크로네</option>
        <option value="EUR">EUR - 유로</option>
        <option value="GBP">GBP - 영국 파운드</option>
        <option value="HKD">HKD - 홍콩 달러</option>
        <option value="IDR(100)">IDR(100) - 인도네시아 루피아</option>
        <option value="JPY(100)">JPY(100) - 일본 옌</option>
        <option value="KWD">KWD - 쿠웨이트 디나르</option>
        <option value="MYR">MYR - 말레이시아 링기트</option>
        <option value="NOK">NOK - 노르웨이 크로네</option>
        <option value="NZD">NZD - 뉴질랜드 달러</option>
        <option value="SAR">SAR - 사우디아라비아 리얄</option>
        <option value="SEK">SEK - 스웨덴 크로나</option>
        <option value="SGD">SGD - 싱가포르 달러</option>
        <option value="THB">THB - 태국 바트</option>
        <option value="USD">USD - 미국 달러</option>
      </select>
      <br>
      <div class="target-rate">
        <label for="rate-input">목표 환율 : </label>
        <input id="rate-input" v-model="targetRate" type="number" class="input" :placeholder="placeholderText" />
        <button type="submit" class="button">알림 설정</button>
      </div>
    </form>
    <p v-if="alertSet" class="success-message">환율 알림이 설정되었습니다!</p>

    <h2 class="title">현재 환율 정보</h2>
    <button @click="fetchExchangeRate" class="button fetch-button">환율 가져오기</button>
    <div v-if="exchangeRate !== null" class="rate-card">
      <p>{{ targetCurrency }} 기준 환율 (KRW): {{ exchangeRate }}</p>
      <p v-if="showAlert" class="alert-message">환율이 목표 이하로 내려갔습니다!</p>
    </div>
    <div v-else>
      <p class="error-message">환율 정보를 불러올 수 없습니다. 다시 시도해 주세요.</p>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, computed } from 'vue';

const currency = ref('');
const targetRate = ref(null);
const exchangeRate = ref(null);
const alertSet = ref(false);
const showAlert = ref(false);
const targetCurrency = ref('');

const placeholderText = computed(() => {
  return targetRate.value ? `목표 환율 : ${targetRate.value}` : "목표 환율";
});

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
    console.log(response); // 추가된 디버깅 로그
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
  if (!currency.value) {
    alert("환율을 알아볼 외화를 선택하세요.");
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/accounts/check_exchange_rate/?currency=${currency.value}`);
    const data = await response.json();

    if (response.ok) {
      if (data.current_rate !== undefined) {
        exchangeRate.value = data.current_rate;
        showAlert.value = data.alert;
        targetCurrency.value = currency.value;
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
</script>

<style scoped>
.exchange-container {
  max-width: 600px;
  margin: 50px auto; /* 상단 간격 추가 */
  padding: 30px;
  background: #ffffff; /* 흰색 배경 */
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15); /* 그림자 강조 */
  border: 2px solid #004aad; /* 테두리 추가 */
}

.title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 20px;
  text-align: center;
}

.alert-form {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px; /* 폼과 아래 콘텐츠 간격 */
}

.select {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #d0d7e6;
  border-radius: 5px;
  background: #f9fbff;
  transition: border-color 0.3s ease;
}

.select:focus {
  border-color: #004aad;
  outline: none;
}

.input {
  padding: 12px;
  font-size: 1rem;
  border: 1px solid #d0d7e6;
  border-radius: 5px;
  background: #f9fbff;
  transition: border-color 0.3s ease;
}

.input:focus {
  border-color: #004aad;
  outline: none;
}

.button {
  padding: 12px 20px;
  font-size: 1rem;
  background-color: #e38e49;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s ease;
}

.button:hover {
  background-color: #ffb172;
}

.fetch-button {
  width: 100%;
  padding: 12px 20px;
  font-size: 1rem;
  background-color: #397edb;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.fetch-button:hover {
  background-color: #265ba8;
}

.success-message {
  color: #28a745;
  font-size: 1rem;
  text-align: center;
  font-weight: bold;
}

.error-message {
  margin-top: 10px;
  font-weight: bold;
  color: #dc3545;
  font-size: 1rem;
  text-align: center;
}

.rate-card {
  color: #000;
  background: #f9fbff;
  font-weight: bold;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #d0d7e6;
  margin-top: 20px;
  text-align: center;
}

.alert-message {
  color: #e38e49;
  font-weight: bold;
  margin-top: 10px;
}

.target-rate{
  color:#000
}
</style>
