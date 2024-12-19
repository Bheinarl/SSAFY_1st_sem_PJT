<template>
  <header>
    <Navbar />
  </header>
  <div class="board-container">
    <h1 class="board-title">📌게시판📌</h1>
    <h6 id="notice">나만의 금융 상품 후기를 공유하고, 나와 비슷한 투자 성향을 가진 사람들의 추천을 확인해보세요! <br> 모의투자 게임 점수를 높일 수 있는 꿀팁도 함께 나눠보세요!</h6>
    <router-link to="/posts/new" class="create-link">글 작성하기</router-link>
    <div class="post-list">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <router-link :to="`/posts/${post.id}`" class="post-title">{{ post.title }}</router-link>
        <div class="post-author">
          <img :src="post.author_profile_picture" alt="Author's profile picture" class="author-profile-pic" @error="handleImageError" />
          <span>작성자 : {{ post.author }}</span>
        </div>
        <p class="post-likes">좋아요 : {{ post.likes }}</p>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';

// 게시글 데이터
const posts = ref([]);

// 게시글 불러오기
const fetchPosts = async () => {
  try {
    const response = await fetch(`${process.env.VITE_API_BASE_URL}api/posts/list/`);
    if (response.ok) {
      posts.value = await response.json();
    } else {
      console.error('Error fetching posts:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
};

const handleImageError = (event) => {
  console.log("Image failed to load:", event.target.src);  // 이미지 URL 출력
  event.target.src = '/default-user.png';   // 이미지가 없을 경우 기본 이미지로 대체
};

// 컴포넌트가 마운트될 때 게시글을 가져옴
onMounted(() => {
  fetchPosts();
});
</script>
<style scoped>

/* 전체 게시판 컨테이너 */
.board-container {
  width: 800px;
  min-height: calc(100vh - 100px); /* 화면 높이를 기준으로 계산 */
  max-height: calc(100vh - 50px); /* 최대 높이도 설정 */
  overflow: hidden; /* 내부 스크롤을 컨트롤 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
  margin: 20px auto;
  padding: 20px;
  background-color: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

.board-container h6{
  font-size: 0.9rem;
  color: #e38e49;
  text-align: center;
  font-weight: bold;
}

/* 게시판 제목 */
.board-title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 20px;
}

/* 글 작성하기 링크 */
.create-link {
  display: inline-block;
  margin-bottom: 20px;
  padding: 10px 15px;
  background-color: #004aad;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  font-size: 0.9rem;
  font-weight: bold;
}

.create-link:hover {
  background-color: #00337c;
}

/* 게시글 리스트: 3열 배치 */
.post-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr); /* 2열 */
  gap: 20px; /* 카드 간격 */
  overflow-y: auto; /* 스크롤 가능 */
  height: calc(100vh - 300px); /* 부모 높이에 맞게 조정 */
  box-sizing: border-box;

}

/* 게시글 카드 */
.post-card {
  background-color: white;
  border: 1px solid #d0d7e6;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

/* 게시글 제목 */
.post-title {
  font-size: 1.2rem;
  font-weight: bold;
  color: #004aad;
  text-decoration: none;
  margin-bottom: 10px;
  display: block;
}

.post-title:hover {
  text-decoration: underline;
}

/* 게시글 작성자 */
.post-author {
  font-size: 0.9rem;
  color: #397edb;
  margin-bottom: 5px;
}

.author-profile-pic {
  width: 30px;
  height: 30px;
  border-radius: 50%; /* 원형 */
  object-fit: cover; /* 비율 유지 및 잘림 */
  margin-right: 8px; /* 텍스트와 간격 */
  vertical-align: middle; /* 텍스트와 정렬 */
}

/* 게시글 좋아요 수 */
.post-likes {
  font-size: 0.9rem;
  color:#e38e49;
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .post-list {
    grid-template-columns: repeat(2, 1fr); /* 2열 */
  }
}

@media screen and (max-width: 480px) {
  .post-list {
    grid-template-columns: 1fr; /* 1열 */
  }
}
</style>
