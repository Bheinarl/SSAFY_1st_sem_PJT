<template>
  <div class="login">
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff; /* 기본 텍스트 색상 */
  font-family: 'Arial', sans-serif;
  text-align: center;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #D4EBF8; /* 제목 텍스트 밝은 파란색 */
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 400px;
}

input {
  padding: 0.75rem;
  border: 2px solid #D4EBF8; /* 밝은 파란색 테두리 */
  border-radius: 8px;
  font-size: 1rem;
  color: #0A3981; /* 입력 텍스트 색상 */
  background-color: #D4EBF8; /* 입력 배경색 */
  outline: none;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #E38E49; /* 포커스 시 테두리 색상 변경 */
}

button {
  padding: 0.75rem 1.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #fff;
  background-color: #E38E49; /* 버튼 배경색: 따뜻한 주황색 */
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

button:hover {
  background-color: #D4EBF8; /* 호버 시 밝은 파란색으로 변경 */
  color: #0A3981; /* 텍스트 색상 변경 */
  transform: scale(1.05); /* 약간 확대 */
}

button:active {
  transform: scale(0.95); /* 클릭 시 눌리는 효과 */
}
</style>
