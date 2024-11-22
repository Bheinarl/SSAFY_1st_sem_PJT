<template>
    <!-- 카테고리 탭 -->
    <nav class="tabs">
      <button v-for="tab in tabs" :key="tab.name" :class="{ active: selectedTab === tab.name }" @click="selectTab(tab.name)">
        {{ tab.label }}
      </button>
    </nav>

    <!-- 페이지네이션 -->
    <div class="pagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage <= 1">이전</button>
      <span>페이지 {{ currentPage }} / {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage >= totalPages">다음</button>
    </div>

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

const selectedTab = ref('deposits'); // 초기 선택 탭은 'deposits'
const products = ref({
  deposits: [],
  savings: [],
  funds: [],
  taxes: [],
});

const pagination = ref({
  total_count: 0,
  max_page_no: 1,
  now_page_no: 1,
});

// 탭 선택 함수
const selectTab = (tabName) => {
  selectedTab.value = tabName;
  fetchProducts();  // 탭 변경 시 데이터 새로 불러오기
};

const currentPage = ref(1);
const totalPages = computed(() => pagination.value.max_page_no);

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchProducts();  // 페이지 변경 시 데이터 새로 불러오기
  }
};

// API를 통해 데이터 불러오기
const fetchProducts = async () => {
  try {
    const endpoint = `http://127.0.0.1:8000/finances/api/products/${selectedTab.value}/`;
    
    const response = await axios.get(endpoint, {
      params: { page: currentPage.value }  // 페이지 번호 전달
    });

    // 선택된 탭에 맞는 데이터를 저장
    products.value[selectedTab.value] = response.data.products;
    pagination.value = response.data.pagination;
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
  fetchProducts(); // 초기 데이터 불러오기
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
