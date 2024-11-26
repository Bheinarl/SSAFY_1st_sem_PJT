<template>
  <div class="home">
    <h1>환영합니다!</h1>
    <p>회원가입 또는 로그인을 진행해주세요.</p>

    <!-- 회원가입 버튼 -->
    <button @click="goToRegister" class="btn btn-primary">회원가입</button>
    <!-- 로그인 버튼 -->
    <button @click="goToLogin" class="btn btn-success">로그인</button>
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
  text-align: center;
}

button {
  margin: 1rem;
  padding: 0.5rem 2rem;
  font-size: 1.2rem;
}
</style>
