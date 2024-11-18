<template>
  <div>
    <h2>주식 데이터</h2>
    <p>데이터 출력 {{ stocks }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const stocks = ref({});

const fetchProfile = async () => {
  try {
    const response = await api.get('/api/auth/user/');
    stocks.value = response.data;
  } catch (error) {
    console.error('Error fetching profile data:', error);
    alert('Failed to load profile information. Please try again.');
  }
};

onMounted(() => {
  fetchProfile();
});
</script>

<style lang="scss" scoped>

</style>