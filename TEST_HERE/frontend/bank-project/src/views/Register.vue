<template>
  <div>
    <h2>회원가입</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <input v-model="password2" type="password" placeholder="Confirm Password" />
    <button @click="register">회원가입</button>
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
    localStorage.setItem('token', response.data.key);
    router.push('/'); // 회원가입 후 리디렉션
  } catch (error) {
    console.error('회원가입 실패:', error.response.data);
  }
};
</script>