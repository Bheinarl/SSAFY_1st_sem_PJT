<template>
  <div class="register">
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
    const response = await axios.post('http://127.0.0.1:8000/api/auth/registration/', {
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff; /* 텍스트 기본 색상 */
  font-family: 'Arial', sans-serif;
  text-align: center;
}

h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #D4EBF8; /* 제목은 밝은 파란색 */
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
