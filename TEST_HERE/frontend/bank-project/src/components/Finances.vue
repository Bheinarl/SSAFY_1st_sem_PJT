<template>
  <div>
    <h1>상품 목록</h1>
    
    <!-- 카테고리 탭 -->
    <div>
      <button @click="fetchProducts('deposits')" :class="{ active: selectedCategory === 'deposits' }">정기예금</button>
      <button @click="fetchProducts('savings')" :class="{ active: selectedCategory === 'savings' }">적금</button>
    </div>

    <!-- 로딩 상태 표시 -->
    <div v-if="loading">로딩 중...</div>

    <!-- 에러 메시지 표시 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 상품 목록 -->
    <table v-if="paginatedProducts.length > 0">
      <thead>
        <tr>
          <th>상품명</th>
          <th>금융회사명</th>
          <th>가입대상</th>
          <th>만기 후 이자율</th>
          <th>가입방법</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(product, index) in paginatedProducts" :key="index">
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.join_member }}</td>
          <td>{{ product.mtrt_int }}</td>
          <td>{{ product.join_way }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div v-if="pagination.total_count > 0">
      <button @click="changePage(pagination.now_page_no - 1)" :disabled="pagination.now_page_no === 1">이전</button>
      <span>{{ pagination.now_page_no }} / {{ pagination.max_page_no }}</span>
      <button @click="changePage(pagination.now_page_no + 1)" :disabled="pagination.now_page_no === pagination.max_page_no">다음</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 상태 변수
const selectedCategory = ref('deposits');  // 기본 카테고리 설정
const products = ref([]);  // 상품 데이터
const paginatedProducts = ref([]);  // 페이지네이션된 상품 데이터
const loading = ref(false);  // 로딩 상태
const error = ref(null);  // 에러 상태
const pagination = ref({
  total_count: 0,
  max_page_no: 1,
  now_page_no: 1,
});

// 카테고리 선택 시 데이터 가져오기
const fetchProducts = async (category) => {
  loading.value = true;
  error.value = null;
  selectedCategory.value = category;  // 카테고리 변경

  try {
    const response = await axios.get(`http://127.0.0.1:8000/finances/api/products/${category}/`);

    if (response.data && response.data.products) {
      products.value = response.data.products;
      paginateProducts();  // 페이지네이션 처리
    } else {
      error.value = "상품을 불러오는 데 실패했습니다.";
    }
  } catch (err) {
    error.value = "상품을 불러오는 중 오류가 발생했습니다.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// 페이지네이션 함수
const paginateProducts = () => {
  const start = (pagination.value.now_page_no - 1) * 20;
  const end = start + 20;
  paginatedProducts.value = products.value.slice(start, end);

  pagination.value.total_count = products.value.length;
  pagination.value.max_page_no = Math.ceil(products.value.length / 20);
};

// 페이지 변경 함수
const changePage = (pageNo) => {
  if (pageNo < 1 || pageNo > pagination.value.max_page_no) return;
  pagination.value.now_page_no = pageNo;
  paginateProducts();  // 새 페이지에 맞는 데이터 업데이트
};

// 컴포넌트가 마운트될 때 기본적으로 데이터 가져오기
onMounted(() => {
  fetchProducts(selectedCategory.value);
});
</script>

<style scoped>
nav {
  display: flex;
  margin-bottom: 20px;
}

nav button {
  padding: 10px 20px;
  margin-right: 10px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  cursor: pointer;
}

nav button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.table-container {
  margin-top: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead th {
  background-color: #5b6269;
  color: white;
  padding: 10px;
  border: 1px solid #c2bd77;
}

tbody td {
  border: 1px solid #b82c2c;
  padding: 10px;
}

.no-data {
  margin-top: 20px;
  color: gray;
  text-align: center;
}
</style>
