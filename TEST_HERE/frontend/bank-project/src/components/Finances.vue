<template>
  <header><Navbar /></header>
  <div class="product-page">

  <!-- 투자자 유형 표시 -->
  <div class="investor-type">
    <h2 class="investor-heading">
      투자자 유형 : 
      <span v-if="userType" class="highlight">{{ userType }}</span>
      <span v-else class="no-type">아직 게임을 하지 않았습니다!</span>
    </h2>
    <p v-if="!userType" class="investor-description">
      모의투자게임을 통해 당신에게 맞는 펀드를 추천받으세요.
    </p>
    <button v-if="!userType" @click="goToGame" class="btn primary-btn">게임하러가기</button>
  </div>



    <!-- 카테고리 탭 -->
    <nav class="category-nav">

      <div>
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
      </div>


      <div class="category-info">
        <template v-if="selectedCategory === 'funds'">
          <!-- 😌🧐😏🤑 -->
          안정 추구형😌 / 균형 투자형🧐 / 공격 투자형😏 / 투기형🤑 <br> 4가지 유형별 맞춤 상품이 강조되어 표시됩니다!
        </template>
        <template v-else-if="selectedCategory === 'deposits' || selectedCategory === 'savings'">
          
          <span>💡 당신이 원하는 상품, 집에 가는 길에 가입하고 싶다면?<br>
          원하는 상품의 <span class="highlight-1">금융회사명</span>을 클릭하여 가장 가까운 지점을 확인하세요.<br></span>

          <span>💡 현재 위치 기준으로 다른 은행을 검색하고 싶다면 <span class="highlight-2">아래 버튼</span>을 클릭하세요.</span>
          <button @click="goToMapView" class="btn map-btn">지도에서 보기</button>
        </template>
      </div>

    </nav>

    <!-- 서브카테고리 -->
    <div v-if="selectedCategory === 'funds' && showFundsSubcategories" class="subcategory-nav">
      <button 
        v-for="subcategory in fundSubcategories" 
        :key="subcategory" 
        @click="changeSubCategory(subcategory)"
        :class="['subcategory-btn', getSubcategoryClass(subcategory)]"
        :style="{ 
  backgroundColor: getSubcategoryClass(subcategory) === 'usertype-selected' ? '#E38E49' : '',
  borderColor: getSubcategoryClass(subcategory) === 'usertype-selected' ? '#E38E49' : ''

         }"
      >
        {{ subcategory }}
      </button>
    </div>

    <!-- 로딩 상태 -->
    <div v-if="loading" class="loading">로딩 중...</div>

    <!-- 에러 메시지 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 상품 카드 -->
    <div class="product-list">
      <div 
        v-for="(product, index) in paginatedProducts" 
        :key="index" 
        class="product-card"
      >
        <h3 class="product-name">{{ product.fin_prdt_nm || product.fndNm }}</h3>
        <p v-if="selectedCategory !== 'funds'">
          금융회사명: 
          <span 
            class="clickable" 
            @click="searchInMap(product.kor_co_nm)"
          >
            {{ product.kor_co_nm }}
          </span>
        </p>
        <p v-if="selectedCategory !== 'funds'">가입대상: {{ product.join_member }}</p>
        <p v-if="selectedCategory !== 'funds'">만기 후 이자율: {{ product.mtrt_int }}</p>
        <p v-if="selectedCategory !== 'funds'">가입방법: {{ product.join_way }}</p>
        <p v-if="selectedCategory === 'funds'">펀드 유형: {{ product.fndTp }}</p>
        <a 
          v-if="selectedCategory === 'funds'" 
          :href="'https://www.funddoctor.co.kr/afn/fund/fprofile.jsp?fund_cd=' + product.asoStdCd" 
          target="_blank"
          class="details-link"
        >
          자세히 보기
        </a>
      </div>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="pagination.total_count > 0">
      <button 
        @click="changePage(pagination.now_page_no - 1)" 
        :disabled="pagination.now_page_no === 1"
        class="pagination-btn"
      >
        이전
      </button>
      <span class="pagination-info">{{ pagination.now_page_no }} / {{ pagination.max_page_no }}</span>
      <button 
        @click="changePage(pagination.now_page_no + 1)" 
        :disabled="pagination.now_page_no === pagination.max_page_no"
        class="pagination-btn"
      >
        다음
      </button>
    </div>



  </div>
</template>


<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

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

// MapView로 이동하는 함수
const goToMapView = () => {
  window.location.href = '/mapview';
};

// Game으로 이동하는 함수
const goToGame = () => {
  window.location.href = '/gamereal';
};



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
  } catch (error) {
    console.error('사용자 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 사용자의 투자 유형에 따라 서브카테고리별 색상 클래스를 반환
const getSubcategoryClass = (subcategory) => {
  if (userType.value === '안정 추구형') {
    if (['채권형', '단기금융'].includes(subcategory)) {
      return 'usertype-selected';
    }
  } else if (userType.value === '균형 투자형') {
    if (['혼합채권형', '혼합자산', '변액보험'].includes(subcategory)) {
      return 'usertype-selected';
    }
  } else if (userType.value === '공격 투자형') {
    if (['주식형', '혼합주식형'].includes(subcategory)) {
      return 'usertype-selected';
    }
  } else if (userType.value === '투기형') {
    if (['재간접', '파생상품', '부동산', '특별자산'].includes(subcategory)) {
      return 'usertype-selected';
    }
  }
  return ''; // 기본값은 빈 문자열
};

// 컴포넌트가 마운트될 때 기본적으로 데이터 가져오기
onMounted(async() => {
  await loadCurrentUser();
  fetchProducts(selectedCategory.value);
});

// KakaoMap.vue로 키워드를 전달하며 이동
const searchInMap = (keyword) => {
  router.push({ path: '/mapview', query: { keyword } });
};

</script>

<style scoped>
.investor-type {
  text-align: center;
  margin-bottom: 30px;
  color: #ffffff; /* 기본 텍스트 색상 */
}

.investor-heading {
  font-size: 1.5rem; /* 제목 크기 */
  font-weight: bold;
  margin-bottom: 10px;
}

.highlight {
  color: #E38E49; /* 강조 텍스트 색상 */
}

.highlight-1 {
  color: #E38E49; /* 강조 색상 */
  font-weight: bold; /* 굵게 */
  text-decoration: underline; /* 밑줄 */
}

.highlight-2 {
  color: #fcd666; /* 강조 색상 */
  font-weight: bold; /* 굵게 */
}

.no-type {
  color: #D4EBF8; /* 텍스트 색상 통일 */
}

.investor-description {
  font-size: 1rem;
  margin-bottom: 15px; /* 설명 텍스트 간격 */
}

.primary-btn {
  padding: 12px 24px;
  background-color: #E38E49; /* 버튼 배경색 */
  color: #ffffff; /* 버튼 텍스트 색상 */
  border: none;
  border-radius: 25px; /* 둥근 버튼 스타일 */
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn:hover {
  background-color: #D4EBF8; /* 호버 시 밝은 파란색 배경 */
  color: #0A3981; /* 호버 시 텍스트 색상 */
}

.primary-btn:focus {
  outline: 3px solid #D4EBF8; /* 포커스 시 강조 */
}

.category-nav {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.category-info {
  background-color: #ffffff; /* 배경색 변경 */
  color: #1F509A; /* 텍스트 색상 */
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  text-align: center;
}

.category-info ul {
  list-style-type: disc;
  margin: 0 0 10px 20px;
  padding: 0;
  font-size: 0.9rem;
}

.category-info ul li {
  margin-bottom: 5px;
}

.map-btn {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #fcd666 !important;
  /* color: #000000  */
  border: 1px solid #fcd666 !important;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.map-btn:hover {
  background-color: #ffe082 !important;
  border: 1px solid #ffe082 !important;
  color: #fff;
}

.category-buttons {
  display: flex;
  flex-direction: row;
  gap: 10px;
  justify-content: center; /* 버튼을 가운데 정렬 */
}

.category-buttons button {
  padding: 10px 20px;
  border: 1px solid #D4EBF8;
  border-radius: 5px;
  background-color: #D4EBF8;
  color: #0A3981;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-buttons button.active {
  background-color: #E38E49;
  color: #fff;
  border-color: #E38E49;
}

.category-buttons button:hover {
  background-color: #E38E49;
  color: #fff;
}

.category-description {
  margin-top: -10px;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #ffffff;
  text-align: center;
  background-color: rgba(228, 115, 45, 0.8);
  padding: 5px 10px;
  border-radius: 5px;
}

.product-page {
  padding: 20px;
  background-color: #1F509A; /* 메인 배경색 */
  color: #fff; /* 기본 텍스트 색상 */
  height: 100vh; /* 화면 높이 고정 */
  overflow-y: auto; /* 세로 스크롤 활성화 */
}

.top-section {
  text-align: center;
  margin-bottom: 20px;
}

.investor-type {
  text-align: center;
  margin-bottom: 30px;
}

.investor-type h2 {
  font-size: 1.5rem;
  color: #D4EBF8;
}

.investor-type .highlight {
  color: #E38E49;
  font-weight: bold;
}

.category-nav, .subcategory-nav {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.category-nav button, .subcategory-btn {
  padding: 10px 20px;
  border: 1px solid #D4EBF8;
  border-radius: 5px;
  background-color: #D4EBF8;
  color: #0A3981;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.category-nav button.active, .subcategory-btn:hover {
  background-color: #E38E49;
  color: #ffffff;
  border-color: #E38E49;
}

.product-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px;
}

.product-card {
  background-color: #fff;
  color: #000;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
}

.product-card .product-name {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #1F509A;
}

.product-card p {
  margin: 5px 0;
  font-size: 0.9rem;
  color: #333;
}

.product-card .clickable {
  color: #E38E49;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
}

.product-card .details-link {
  display: inline-block;
  margin-top: 10px;
  font-size: 0.9rem;
  color: #1F509A;
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
}

.pagination {
  display: flex;
  justify-content: center; /* 가운데 정렬 */
  align-items: center;
  gap: 10px; /* 버튼 사이 간격 */
  margin-top: 20px; /* 위쪽 여백 */
  padding: 10px 0; /* 전체 컨테이너 패딩 */
}

.pagination-btn {
  padding: 10px 15px;
  border: 1px solid #D4EBF8;
  background-color: #D4EBF8;
  color: #0A3981;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.pagination-btn:disabled {
  background-color: #ccc; /* 비활성화 상태 배경 */
  color: #666; /* 비활성화 상태 텍스트 */
  cursor: not-allowed;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #E38E49;
  color: #fff;
}

.pagination-info {
  font-size: 1rem;
  font-weight: bold;
  color: #ffffff;
}

.usertype-selected {
  padding: 10px 20px;
  border: 1px solid #D4EBF8;
  border-radius: 5px;
  background-color: #D4EBF8;
  color: #0A3981;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

</style>
