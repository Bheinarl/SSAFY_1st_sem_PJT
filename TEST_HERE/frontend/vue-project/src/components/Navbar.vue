<template>
    <nav>
        <router-link to="/">Home</router-link> |
        <router-link v-if="!isAuthenticated" to="/register">Register</router-link> |
        <router-link v-if="!isAuthenticated" to="/login">Login</router-link> |
        <router-link v-if="isAuthenticated" to="/profile">Profile</router-link> |
        <button v-if="isAuthenticated" @click="logout">Logout</button>
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
