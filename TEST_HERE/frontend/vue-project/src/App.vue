<template>
  <div id="app">
      <Navbar /> <!-- Navbar 컴포넌트 추가 -->
      <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
      Navbar
  }
};
</script>

<style>
/* 전역 스타일을 여기에 추가할 수 있습니다. */
</style>


<!-- 
<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/profile">Profile</router-link>
    </nav>
    <router-view></router-view> 
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
nav {
  margin-bottom: 20px;
}
</style> -->
