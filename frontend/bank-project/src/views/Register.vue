<template>
  <div>
      <h2>Sign Up</h2>
      <form @submit.prevent="register">
          <label>Username:</label>
          <input v-model="username" type="text" required />

          <label>Nickname:</label>
          <input v-model="nickname" type="text" required />

          <label>Password:</label>
          <input v-model="password1" type="password" required />

          <label>Confirm Password:</label>
          <input v-model="password2" type="password" required />

          <label>Age : </label>
          <input v-model="age" type="number" /><br>

          <button type="submit">Register</button>
      </form>
      <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>

<script>
import api from '../api';

export default {
  data() {
      return {
          username: '',      // 사용자 이름
          nickname: '',      // 별명
          password1: '',     // 비밀번호
          password2: '',     // 비밀번호 확인
          age: null,         // 나이
          error: null,       // 오류 메시지
      };
  },
  methods: {
    async register() {
      try {
        const requestData = {
              username: this.username,
              nickname: this.nickname,
              password1: this.password1,
              password2: this.password2,
          };
          if (this.age !== null) {
              requestData.age = this.age;
          }
          const response = await api.post('/api/auth/custom-registration/', requestData);
          console.log('Registration successful:', response.data);
          alert('Registration successful! Redirecting to login...');
          this.$router.push('/login'); // 회원가입 성공 후 로그인 페이지로 이동
      } catch (error) {
          this.error = 
              error.response?.data?.nickname?.[0] ||
              error.response?.data?.non_field_errors?.[0] ||
              error.response?.data?.password1?.[0] ||
              'Registration failed!';
          console.error('Registration failed:', error.response?.data || error);
      }
  }

    // async register() {
    //   try {
    //       const response = await api.post('/api/auth/custom-registration/', {
    //           username: this.username,
    //           nickname: this.nickname,
    //           password1: this.password1,
    //           password2: this.password2,
    //       });
    //       console.log('Registration successful:', response.data);
    //       alert('Registration successful! Redirecting to login...');
    //       this.$router.push('/login'); // 회원가입 성공 후 로그인 페이지로 이동
    //   } catch (error) {
    //       this.error = 
    //           error.response?.data?.nickname?.[0] ||
    //           error.response?.data?.non_field_errors?.[0] ||
    //           error.response?.data?.password1?.[0] ||
    //           'Registration failed!';
    //       console.error('Registration failed:', error.response?.data || error);
    //   }
    // }
  },
};
</script>

<style scoped>
/* 필요한 경우 스타일 추가 */
</style>
