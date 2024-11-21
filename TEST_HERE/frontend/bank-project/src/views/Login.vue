<template>
  <div>
    <h2>로그인</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">로그인</button>
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
    console.log('토큰은 이렇습니다.', response.data.key);
    router.push('/'); // 로그인 후 리디렉션
  } catch (error) {
    console.error('로그인 실패:', error.response.data);
  }
};
</script>