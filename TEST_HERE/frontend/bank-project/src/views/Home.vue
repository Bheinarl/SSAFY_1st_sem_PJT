<template>
  <div class="home">
    <div class="welcome-container">
      <h1>환영합니다!</h1>
      <p>회원가입 또는 로그인을 진행해주세요.</p>
    </div>

    <div class="button-container">
      <!-- 회원가입 버튼 -->
      <button @click="goToRegister" class="btn register-btn">회원가입</button>
      <!-- 로그인 버튼 -->
      <button @click="goToLogin" class="btn login-btn">로그인</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import axios from 'axios';

const router = useRouter();

// 기존 데이터 로드 함수들
async function updateStockUrl() {
  const apiUrl = 'http://127.0.0.1:8000/stocks/api/stocks/list/';
  console.log('API URL:', apiUrl);
  try {
    await axios.get(apiUrl);
  } catch (error) {
    console.error('Error fetching stock data:', error);
  }
}

const fetchDataAndSaveDeposits = async () => {
  try {
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/deposits');
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

const fetchDataAndSaveSavings = async () => {
  try {
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/savings');
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

const fetchDataAndSaveFunds = async () => {
  try {
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/funds');
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

// onMounted에서 기존 기능 호출
onMounted(async () => {
  await updateStockUrl();
  await fetchDataAndSaveDeposits();
  await fetchDataAndSaveSavings();
  await fetchDataAndSaveFunds();
});

// 회원가입 및 로그인 버튼 동작
const goToRegister = () => {
  router.push('/register'); // 회원가입 페이지로 이동
};

const goToLogin = () => {
  router.push('/login'); // 로그인 페이지로 이동
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff; /* 기본 텍스트 색상 */
  text-align: center;
  font-family: 'Arial', sans-serif;
}

.welcome-container h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  color: #D4EBF8; /* 제목 텍스트를 밝은 파란색으로 설정 */
}

.welcome-container p {
  font-size: 1.2rem;
  color: #E38E49; /* 부드러운 주황색으로 서브 텍스트 강조 */
  margin-bottom: 2rem;
}

.button-container {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
}

button {
  border: none;
  border-radius: 12px;
  padding: 0.75rem 2.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.register-btn {
  background-color: #D4EBF8; /* 회원가입 버튼: 밝은 파란색 */
  color: #0A3981; /* 텍스트를 짙은 파란색으로 */
}

.register-btn:hover {
  background-color: #E38E49; /* 호버 시 따뜻한 주황색 */
  color: #fff; /* 텍스트를 흰색으로 */
  transform: scale(1.05); /* 약간의 확대 효과 */
}

.login-btn {
  background-color: #E38E49; /* 로그인 버튼: 따뜻한 주황색 */
  color: #fff; /* 텍스트는 흰색 */
}

.login-btn:hover {
  background-color: #D4EBF8; /* 호버 시 밝은 파란색 */
  color: #0A3981; /* 텍스트는 짙은 파란색 */
  transform: scale(1.05);
}

button:active {
  transform: scale(0.95); /* 클릭 시 눌리는 효과 */
}
</style>
