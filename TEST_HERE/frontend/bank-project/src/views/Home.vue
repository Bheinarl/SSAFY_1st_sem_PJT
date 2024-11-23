<template>
  <div>
    <h1>Home Page</h1>
    <p>Welcome to the home page!</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import axios from 'axios';

const fetchDataAndSaveDeposits = async () => {
  try {
    // 백엔드로 데이터를 요청하여 수신 및 저장
    await axios.get('/api/fetch-and-save-products/deposits');  // 데이터를 백엔드에서 수신하고 저장하는 API
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

const fetchDataAndSaveSavings = async () => {
  try {
    // 백엔드로 데이터를 요청하여 수신 및 저장
    await axios.get('/api/fetch-and-save-products/savings');  // 데이터를 백엔드에서 수신하고 저장하는 API
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

onMounted(() => {
  fetchDataAndSaveDeposits(); // Home.vue가 로드될 때 데이터 수신 및 저장
  fetchDataAndSaveSavings(); // Home.vue가 로드될 때 데이터 수신 및 저장
});
</script>

<style scoped>
/* 페이지 전용 스타일 추가 가능 */
</style>
