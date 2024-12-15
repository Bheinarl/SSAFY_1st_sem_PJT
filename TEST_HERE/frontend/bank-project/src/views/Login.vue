<template>
  <div class="login">
    <div class="background-shapes">
      <div class="circle-large"></div>
      <div class="circle-medium"></div>
      <div class="circle-small"></div>
      <div class="rectangle"></div>
      <div class="triangle"></div>
      <div class="ellipse"></div>
    </div>
    <h2>로그인</h2>
    <div class="form-container">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">로그인</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const router = useRouter();

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: username.value,
      password: password.value,
    });
    console.log('로그인 성공, 토큰:', response.data.key);
    localStorage.setItem('token', response.data.key);

    router.push('/profile'); // 로그인 후 리디렉션
  } catch (error) {
    console.error('로그인 실패:', error.response.data);
  }
};
</script>

<style scoped>
.login {
  position: relative; /* 배경 도형과 콘텐츠를 구분 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff; /* 기본 텍스트 색상 */
  text-align: center;
  overflow: hidden; /* 도형이 화면 밖으로 넘어가지 않도록 */
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

/* 도형 스타일과 애니메이션 */
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
  color: #D4EBF8; /* 밝은 파란색 텍스트 */
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

button:hover {
  background-color: #D4EBF8;
  color: #0A3981;
}

/* 애니메이션 재사용: 도형 움직임 */
@keyframes float-large {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-50px);
  }
}

@keyframes float-medium {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(40px);
  }
}

@keyframes float-small {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes float-rectangle {
  0%, 100% {
    transform: rotate(30deg) translateX(0);
  }
  50% {
    transform: rotate(40deg) translateX(10px);
  }
}

@keyframes float-triangle {
  0%, 100% {
    transform: rotate(30deg) translateX(0);
  }
  50% {
    transform: rotate(33deg) translateX(15px);
  }
}

@keyframes float-ellipse {
  0%, 100% {
    transform: translateY(0) rotate(30deg);
  }
  50% {
    transform: translateY(-20px) rotate(35deg);
  }
}
</style>
