<template>
    <nav>
      <!-- <router-link to="/">Home</router-link><span v-show="!isAuthenticated"> | </span> -->
      <router-link v-show="!isAuthenticated" to="/register">Register</router-link><span v-show="!isAuthenticated"> | </span>
      <router-link v-show="isAuthenticated" to="/profile">Profile</router-link><span v-show="isAuthenticated"> | </span>
      <router-link v-show="isAuthenticated" to="/posts">게시판</router-link><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goGame">goGameReal</button><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goFinances">Finances</button><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="goLeaderBoard">LeaderBoard</button><span v-show="isAuthenticated"> | </span>
      <button v-show="isAuthenticated" @click="logout">Logout</button><span v-show="isAuthenticated"> | </span>
    </nav>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAuthenticated = ref(!!localStorage.getItem('token'));

const logout = () => {
    localStorage.removeItem('token');
    isAuthenticated.value = false;
    router.push('/');
};

const goGame = () => {
    router.push('/gamereal');
};

const goFinances = () => {
    router.push('/finances');
};

const goLeaderBoard = () => {
    router.push('/leaderboard');
};

// 로그인 상태가 변경되면 Navbar 업데이트
watch(() => router.currentRoute, () => {
    isAuthenticated.value = !!localStorage.getItem('token');
});
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