<template>
  <div>
    <h1>Home Page</h1>
    <p>Welcome to the home page!</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import axios from 'axios';

async function updateStockUrl() {
    const apiUrl = 'http://127.0.0.1:8000/stocks/api/stocks/list/';
    console.log('API URL:', apiUrl);
    try {
        const response = await axios.get(apiUrl);
    } catch (error) {
        console.error('Error fetching stock data:', error);
    }
}

const fetchDataAndSaveDeposits = async () => {
  try {
    // 백엔드로 데이터를 요청하여 수신 및 저장
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/deposits');  // 데이터를 백엔드에서 수신하고 저장하는 API
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

const fetchDataAndSaveSavings = async () => {
  try {
    // 백엔드로 데이터를 요청하여 수신 및 저장
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/savings');  // 데이터를 백엔드에서 수신하고 저장하는 API
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

const fetchDataAndSaveFunds = async () => {
  try {
    // 백엔드로 데이터를 요청하여 수신 및 저장
    await axios.get('http://127.0.0.1:8000/finances/api/fetch_and_save_products/funds');  // 데이터를 백엔드에서 수신하고 저장하는 API
    console.log('데이터 수신 및 저장 완료');
  } catch (error) {
    console.error('데이터 수신 실패:', error);
  }
};

onMounted(async () => {
  await updateStockUrl();  // updateStockUrl이 완료된 후
  await fetchDataAndSaveDeposits(); // Home.vue가 로드될 때 데이터 수신 및 저장
  await fetchDataAndSaveSavings(); // Home.vue가 로드될 때 데이터 수신 및 저장
  await fetchDataAndSaveFunds(); // Home.vue가 로드될 때 데이터 수신 및 저장
});

</script>

<style scoped>
/* 페이지 전용 스타일 추가 가능 */
</style>
