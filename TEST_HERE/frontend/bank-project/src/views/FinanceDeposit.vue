<template>
  <div class="finance-page">

    <!-- 데이터가 존재하는 경우 테이블 출력 -->
    <div v-if="currentData.length">
      <table>
        <thead>
          <tr>
            <th>상품명</th>
            <th>은행명</th>
            <th>가입방법</th>
            <th>최대금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in currentData" :key="product.fin_prdt_cd">
            <td>{{ product.fin_prdt_nm }}</td>
            <td>{{ product.kor_co_nm }}</td>
            <td>{{ product.join_way }}</td>
            <td>{{ product.mtrt_int }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>현재 선택된 카테고리에 데이터가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// 탭 데이터
const tabs = [
  { name: 'deposits', label: '정기예금' },
  { name: 'savings', label: '적금' },
  { name: 'funds', label: '펀드' },
  { name: 'tax', label: '절세금융상품' },
];

const selectedTab = ref('deposits');
const products = ref({
  deposits: [],
  savings: [],
  funds: [],
  taxes: [],
});

// 탭 선택 함수
const selectTab = (tabName) => {
  selectedTab.value = tabName;
  fetchProducts();  // 탭 변경 시 데이터 새로 불러오기
};

// API를 통해 데이터 불러오기
const fetchProducts = async () => {
  try {
    const endpoint = `http://127.0.0.1:8000/finances/api/products/${selectedTab.value}/`;
    
    const response = await axios.get(endpoint);

    // 선택된 탭에 맞는 데이터를 저장
    if (selectedTab.value === 'deposits') {
      products.value.deposits = response.data;
    } else if (selectedTab.value === 'savings') {
      products.value.savings = response.data;
    } else if (selectedTab.value === 'funds') {
      products.value.funds = response.data;
    } else if (selectedTab.value === 'tax') {
      products.value.taxes = response.data;
    }
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// 탭에 해당하는 데이터 반환
const currentData = computed(() => {
  return products.value[selectedTab.value] || [];
});

// 컴포넌트가 마운트될 때 데이터 불러오기
onMounted(() => {
  fetchProducts()
  selectTab(tabName)
});
</script>

<style scoped>
.finance-page {
  padding: 20px;
}

.table-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  background-color: #007bff;
  color: white;
  padding: 10px;
}

tbody td {
  border: 1px solid #ccc;
  padding: 10px;
}

.no-data {
  margin-top: 20px;
  color: gray;
  text-align: center;
}
</style>