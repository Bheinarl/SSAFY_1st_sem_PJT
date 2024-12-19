<template>
  <div class="register">
    <div class="background-shapes">
      <div class="circle-large"></div>
      <div class="circle-medium"></div>
      <div class="circle-small"></div>
      <div class="rectangle"></div>
      <div class="triangle"></div>
      <div class="ellipse"></div>
    </div>
    <h2>회원가입</h2>
    <div class="form-container">
      <input v-model="username" placeholder="Username" />
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Password" />
      <input v-model="password2" type="password" placeholder="Confirm Password" />
      <button @click="register">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const email = ref('');
const password = ref('');
const password2 = ref('');
const router = useRouter();

const register = async () => {
  try {
    const response = await axios.post(`${process.env.VITE_API_BASE_URL}api/auth/registration/`, {
      username: username.value,
      password1: password.value,
      password2: password2.value,
      email: email.value,
    });
    console.log('회원가입 성공, 토큰:', response.data.key);
    router.push('/login'); // 회원가입 후 리디렉션
  } catch (error) {
    console.error('회원가입 실패:', error.response.data);
  }
};
</script>

<style scoped>
.register {
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

/* 도형 스타일과 애니메이션은 이전 코드 그대로 재사용 */
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

/* 텍스트 */
h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  z-index: 1; /* 텍스트는 도형 위로 */
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 400px;
  z-index: 1; /* 폼은 도형 위로 */
}

input {
  padding: 0.75rem;
  border: 2px solid #D4EBF8;
  border-radius: 8px;
  font-size: 1rem;
  color: #0A3981;
  background-color: #D4EBF8;
  outline: none;
}

button {
  padding: 0.75rem 1.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #E38E49;
  border: none;
  border-radius: 12px;
  cursor: pointer;
}
</style>
