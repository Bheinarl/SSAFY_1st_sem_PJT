<template>
  <div class="home">
    <div class="background-shapes">
      <div class="circle-large"></div>
      <div class="circle-medium"></div>
      <div class="circle-small"></div>
      <div class="rectangle"></div>
      <div class="triangle"></div>
      <div class="ellipse"></div>
    </div>
    <div class="welcome-container">
      <h1>환영합니다!</h1>
      <p>회원가입 또는 로그인을 진행해주세요.</p>
    </div>

    <div class="button-container">
      <button @click="goToRegister" class="btn register-btn">회원가입</button>
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

const goToRegister = () => {
  router.push('/register');
};

const goToLogin = () => {
  router.push('/login');
};
</script>


<style scoped>
/* 텍스트 컨테이너 */
.welcome-container h1 {
  font-size: 2.5rem;
  color: #D4EBF8; /* 제목은 밝은 파란색 */
  margin-bottom: 0.5rem;
}

.welcome-container p {
  font-size: 1.2rem;
  color: #E38E49; /* 서브 텍스트는 주황색 */
  margin-bottom: 2rem;
}

/* 버튼 컨테이너 */
.button-container {
  display: flex;
  gap: 1.5rem;
  z-index: 1; /* 버튼을 배경보다 위로 설정 */
}

/* 버튼 스타일 */
button {
  padding: 0.75rem 2.5rem;
  border-radius: 8px;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  border: none;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.register-btn {
  background-color: #D4EBF8; /* 회원가입 버튼 */
  color: #0A3981;
}

.register-btn:hover {
  background-color: #E38E49;
  color: #fff;
}

.login-btn {
  background-color: #E38E49; /* 로그인 버튼 */
  color: #fff;
}

.login-btn:hover {
  background-color: #D4EBF8;
  color: #0A3981;
}




/* 홈 컨테이너 스타일 */
.home {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff;
  text-align: center;
  overflow: hidden;
}

/* 배경 도형 컨테이너 */
.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0; /* 배경을 가장 아래로 배치 */
  pointer-events: none; /* 배경 도형 클릭 차단 */
}

/* 큰 원 애니메이션 */
.circle-large {
  position: absolute;
  top: -120px;
  right: -120px;
  width: 400px;
  height: 400px;
  background-color: #D4EBF8;
  border-radius: 50%;
  opacity: 0.5;
  animation: float-large 5s cubic-bezier(0.68, -0.55, 0.27, 1.55) infinite;
}

/* 중간 원 애니메이션 */
.circle-medium {
  position: absolute;
  top: 35%;
  right: 10%;
  width: 250px;
  height: 250px;
  background-color: #E38E49;
  border-radius: 50%;
  opacity: 0.4;
  animation: float-medium 6s ease-in-out infinite alternate;
}

/* 작은 원 애니메이션 */
.circle-small {
  position: absolute;
  bottom: 10%;
  left: 5%;
  width: 150px;
  height: 150px;
  background-color: #D4EBF8;
  border-radius: 50%;
  opacity: 0.6;
  animation: float-small 4s ease-in-out infinite alternate-reverse;
}

/* 사각형 애니메이션 */
.rectangle {
  position: absolute;
  bottom: 20%;
  right: -30px;
  width: 150px;
  height: 150px;
  background-color: #D4EBF8;
  transform: rotate(30deg);
  opacity: 0.5;
  animation: float-rectangle 7s linear infinite;
}

/* 삼각형 애니메이션 */
.triangle {
  position: absolute;
  top: 5%;
  left: 10%;
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-bottom: 100px solid #E38E49;
  opacity: 0.6;
  transform: rotate(30deg);
  animation: float-triangle 5s ease-in-out infinite alternate-reverse;
}

/* 타원 애니메이션 */
.ellipse {
  position: absolute;
  bottom: -50px;
  left: 40%;
  width: 400px;
  height: 200px;
  background-color: #E38E49;
  border-radius: 50%;
  opacity: 0.3;
  transform: rotate(30deg);
  animation: float-ellipse 9s ease-in-out infinite;
}

/* 애니메이션 키프레임 */

/* 큰 원: 위아래로 크게 이동 + 회전 */
@keyframes float-large {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-50px) rotate(360deg);
  }
}

/* 중간 원: 좌우 이동 + 약간의 확대 */
@keyframes float-medium {
  0% {
    transform: translateX(0) scale(1);
  }
  50% {
    transform: translateX(40px) scale(1.1);
  }
  100% {
    transform: translateX(-40px) scale(1);
  }
}

/* 작은 원: 위아래 빠르게 이동 + 축소 */
@keyframes float-small {
  0% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(0.9);
  }
  100% {
    transform: translateY(10px) scale(1);
  }
}

/* 사각형: 좌우 지그재그 + 회전 */
@keyframes float-rectangle {
  0% {
    transform: rotate(30deg) translateX(0);
  }
  25% {
    transform: rotate(35deg) translateX(10px);
  }
  50% {
    transform: rotate(40deg) translateX(-20px);
  }
  75% {
    transform: rotate(35deg) translateX(10px);
  }
  100% {
    transform: rotate(30deg) translateX(0);
  }
}

/* 삼각형: 좌우로 흔들림 + 확대 */
@keyframes float-triangle {
  0%, 100% {
    transform: rotate(30deg) translateX(0) scale(1);
  }
  50% {
    transform: rotate(33deg) translateX(15px) scale(1.1);
  }
}

/* 타원: 위아래 느리게 이동 + 기울기 변경 */
@keyframes float-ellipse {
  0%, 100% {
    transform: translateY(0) rotate(30deg);
  }
  50% {
    transform: translateY(-20px) rotate(35deg);
  }
}

</style>
