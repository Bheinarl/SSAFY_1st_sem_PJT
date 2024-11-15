<template>
    <div>
        <h2>Login</h2>
        <form @submit.prevent="login">
            <label>Username:</label>
            <input v-model="username" type="text" required />
            <label>Password:</label>
            <input v-model="password" type="password" required />
            <button type="submit">Login</button>
        </form>
        <p v-if="error" style="color: red;">{{ error }}</p>
    </div>
</template>

<script>
import api from '../api';

export default {
    data() {
        return {
            username: '',
            password: '',
            error: null,
        };
    },
    methods: {
        async login() {
            try {
                const response = await api.post('/api/auth/login/', {
                    username: this.username,
                    password: this.password,
                });
                console.log('Login successful:', response.data);

                // JWT 토큰 저장
                // localStorage.setItem('token', response.data.key);

                const token = response.data.key;  // 응답에서 토큰 가져오기
                localStorage.setItem('token', token);  // localStorage에 저장
                console.log('Login successful. Token:', token);  // 콘솔에 토큰 출력 - 디버깅용 지우기않기

                alert('Login successful! Redirecting to profile...');
                this.$router.push('/profile'); // 로그인 성공 후 프로필 페이지로 이동
            } catch (error) {
                this.error = 'Login failed. Please check your username and password.';
                console.error('Login failed:', error.response?.data || error);
            }
        },
    },
};
</script>
