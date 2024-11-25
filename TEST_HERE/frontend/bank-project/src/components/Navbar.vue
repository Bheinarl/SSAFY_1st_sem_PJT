<template>
    <nav>
      <router-link to="/">Home</router-link><span v-show="!isAuthenticated"> | </span>
      <router-link v-show="!isAuthenticated" to="/register">Register</router-link><span v-show="!isAuthenticated"> | </span>
      <router-link v-show="isAuthenticated" to="/profile">Profile</router-link><span v-show="isAuthenticated"> | </span>
      <router-link v-show="isAuthenticated" to="/posts">게시판</router-link><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goGame">goGameReal</button><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goFinances">Finances</button><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goLeaderBoard">LeaderBoard</button><span v-show="isAuthenticated"> | </span>
      
      <router-link v-show="!isAuthenticated" to="/login">Login</router-link><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="logout">Logout</button><span v-show="isAuthenticated"> | </span>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            isAuthenticated: !!localStorage.getItem('token')
        };
    },
    methods: {
        logout() {
            localStorage.removeItem('token');
            this.isAuthenticated = false;
            this.$router.push('/login');
        },
        // goExchangeRateAlert() {
        //     this.$router.push('/exchange-rate-alert');
        // },
        goGame() {
            this.$router.push('/gamereal');
        },
        // goFinances() {
        //     this.$router.push('/finances');
        // },
        goLeaderBoard() {
            this.$router.push('/leaderboard');
        }
    },
    watch: {
        // 로그인 상태가 변경되면 Navbar 업데이트
        '$route'() {
            this.isAuthenticated = !!localStorage.getItem('token');
        }
    }
};
</script>

<style scoped>
nav {
    padding: 1em;
    background-color: #f8f9fa;
}
nav a {
    margin-right: 10px;
    text-decoration: none;
    color: #007bff;
}
button {
    background: none;
    border: none;
    color: #007bff;
    cursor: pointer;
}
</style>
