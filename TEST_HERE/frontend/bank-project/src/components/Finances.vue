<template>
  <div>
    <h1>상품 목록</h1>
    
    <!-- 카테고리 탭 -->
    <nav>
      <button 
        @click="changeCategory('funds')" 
        :class="{ active: selectedCategory === 'funds' }"
      >
        펀드
      </button>
      <button 
        @click="changeCategory('deposits')" 
        :class="{ active: selectedCategory === 'deposits' }"
      >
        정기예금
      </button>
      <button 
        @click="changeCategory('savings')" 
        :class="{ active: selectedCategory === 'savings' }"
      >
        적금
      </button>
    </nav>
    <nav>
      <div v-if="selectedCategory === 'funds' && showFundsSubcategories" class="subcategories">
        <button 
          v-for="subcategory in fundSubcategories" 
          :key="subcategory" 
          @click="changeSubCategory(subcategory)"
          :class="getSubcategoryClass(subcategory)"
        >
          {{ subcategory }}
        </button>
      </div>
    </nav>

    <!-- 로딩 상태 표시 -->
    <div v-if="loading">로딩 중...</div>

    <!-- 에러 메시지 표시 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 상품 목록 -->
    <table v-if="paginatedProducts.length > 0">
      <thead>
        <tr v-if="selectedCategory == 'deposits' || selectedCategory == 'savings'">
          <th>상품명</th>
          <th>금융회사명</th>
          <th>가입대상</th>
          <th>만기 후 이자율</th>
          <th>가입방법</th>
        </tr>
        <tr v-else-if="selectedCategory == 'funds'">
          <th>상품명</th>
          <th>펀드 유형</th>
        </tr>
      </thead>
      <tbody v-if="selectedCategory == 'deposits' || selectedCategory == 'savings'">
        <tr v-for="(product, index) in paginatedProducts" :key="index">
          <td>{{ product.fin_prdt_nm }}</td>
          <td>{{ product.kor_co_nm }}</td>
          <td>{{ product.join_member }}</td>
          <td>{{ product.mtrt_int }}</td>
          <td>{{ product.join_way }}</td>
        </tr>
      </tbody>
      <tbody v-else-if="selectedCategory == 'funds'">
        <tr v-for="(product, index) in paginatedProducts" :key="index">
          <td><a :href="'https://www.funddoctor.co.kr/afn/fund/fprofile.jsp?fund_cd=' + product.asoStdCd">{{ product.fndNm }}</a></td>
          <td>{{ product.fndTp }}</td>
        </tr>
      </tbody>
    </table>

    <!-- 페이지네이션 -->
    <div v-if="pagination.total_count > 0">
      <button 
        @click="changePage(pagination.now_page_no - 1)" 
        :disabled="pagination.now_page_no === 1"
      >
        이전
      </button>
      <span>{{ pagination.now_page_no }} / {{ pagination.max_page_no }}</span>
      <button 
        @click="changePage(pagination.now_page_no + 1)" 
        :disabled="pagination.now_page_no === pagination.max_page_no"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 상태 변수
const selectedCategory = ref('funds'); // 기본 카테고리 설정
const selectedSubcategory = ref('전체'); // 기본 서브카테고리 설정
const showFundsSubcategories = ref(true); // 펀드 하위 카테고리 표시 여부

const fundSubcategories = ['전체', '채권형', '단기금융', '혼합채권형', '혼합자산', '변액보험', '혼합주식형', '주식형', '파생상품', '부동산', '특별자산', '재간접']

const products = ref([]); // 전체 상품 데이터
const paginatedProducts = ref([]); // 페이지네이션된 상품 데이터
const loading = ref(false); // 로딩 상태
const error = ref(null); // 에러 상태
const pagination = ref({
  total_count: 0,
  max_page_no: 1,
  now_page_no: 1,
});

// 상품 데이터 가져오기
const fetchProducts = async (category, subcategory = '전체') => {
  loading.value = true;
  error.value = null;
  let apiUrl;

  try {
    if (category === 'funds') {
      apiUrl = `http://127.0.0.1:8000/finances/api/products/funds/${subcategory}/`;
    } else {
      apiUrl = `http://127.0.0.1:8000/finances/api/products/${category}/`;
    }

    const response = await axios.get(apiUrl);

    if (response.data) {
      products.value = response.data.products || [];
      pagination.value.total_count = products.value.length;
      pagination.value.max_page_no = Math.ceil(products.value.length / 10);
      changePage(1); // 첫 페이지로 초기화
    } else {
      error.value = "상품 데이터를 불러오는 데 실패했습니다.";
    }
  } catch (err) {
    error.value = "데이터 요청 중 오류가 발생했습니다.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

// 서브카테고리 변경 시 호출
const changeSubCategory = (subcategory) => {
  selectedSubcategory.value = subcategory;
  fetchProducts('funds', subcategory);
};

// 페이지네이션 데이터 생성
const paginateProducts = () => {
  const start = (pagination.value.now_page_no - 1) * 10; // 현재 페이지의 시작 인덱스
  const end = start + 10; // 현재 페이지의 끝 인덱스
  paginatedProducts.value = products.value.slice(start, end); // 현재 페이지 데이터 추출
};

// 페이지 변경 함수
const changePage = (pageNo) => {
  if (pageNo < 1 || pageNo > pagination.value.max_page_no) return;
  pagination.value.now_page_no = pageNo;
  paginateProducts(); // 페이지 데이터 갱신
};

// 카테고리 변경
const changeCategory = (category) => {
  selectedCategory.value = category;
  selectedSubcategory.value = '전체'; // 기본 서브카테고리로 초기화
  showFundsSubcategories.value = category === 'funds'; // 펀드 하위 카테고리 토글
  fetchProducts(category);
};


const userType = ref(''); // 사용자 유형을 저장할 변수

// 현재 사용자를 저장할 변수
const loadCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    // 토큰이 없으면 로그인 페이지로 리다이렉트
    router.push('/login');
    return;
  }
  
  try {
    const response = await fetch('http://127.0.0.1:8000/accounts/get_current_user/', {
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    userType.value = data.my_investor_type;  // 로그인된 사용자 정보 저장
    // getUserTypeClass(userType.value);
  } catch (error) {
    console.error('사용자 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 사용자의 투자 유형에 따라 서브카테고리별 색상 클래스를 반환
const getSubcategoryClass = (subcategory) => {
  if (userType.value === '안정 추구형') {
    if (['채권형', '단기금융'].includes(subcategory)) {
      return 'green-bg';
    }
  } else if (userType.value === '균형 투자형') {
    if (['혼합채권형', '혼합자산', '변액보험'].includes(subcategory)) {
      return 'blue-bg';
    }
  } else if (userType.value === '공격 투자형') {
    if (['주식형', '혼합주식형'].includes(subcategory)) {
      return 'yellow-bg';
    }
  } else if (userType.value === '투기형') {
    if (['재간접', '파생상품', '부동산', '특별자산'].includes(subcategory)) {
      return 'red-bg';
    }
  }
  return ''; // 기본값은 빈 문자열
};

// 컴포넌트가 마운트될 때 기본적으로 데이터 가져오기
onMounted(async() => {
  await loadCurrentUser();
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
  /* margin-right: 10px; */
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  cursor: pointer;
}

nav button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.green-bg {
  background-color: #90EE90;
  color: black;
}

.blue-bg {
  background-color: #ADD8E6;
  color: black;
}

.yellow-bg {
  background-color: #FFFFE0;
  color: black;
}

.red-bg {
  background-color: #FFCCCB;
  color: black;
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
