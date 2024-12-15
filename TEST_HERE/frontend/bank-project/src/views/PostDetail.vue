<template>
  <header>
    <Navbar />
  </header>
  <div class="post-detail-container">
    <h1 class="post-title">{{ post.title }}</h1>
    <p class="post-meta">
      <div class="post-author">
        <img :src="post.author_profile_picture" alt="Author's profile picture" class="author-profile-pic" @error="handleImageError" />
        <span>작성자: {{ post.author }}</span>
      </div>
      <span class="post-likes">좋아요: {{ post.likes }}</span>
    </p>
    <p class="post-content">{{ post.content }}</p>

    <div class="button-group">
      <button @click="toggleLike" class="like-button">
        {{ isLiked ? '좋아요 취소' : '좋아요' }}
      </button>
      <button v-if="isAuthor"@click="deletePost" class="delete-button">삭제</button>
      <button v-if="isAuthor"@click="editPost" class="edit-button">수정</button>
      
    </div>

    <router-link to="/posts" class="back-link">뒤로가기</router-link>
  </div>
</template>


<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const post = ref({});
const currentUser = ref(localStorage.getItem('username')); // 현재 사용자

// 작성자 확인
const isAuthor = ref(false);
const isLiked = ref(false);

// 데이터 로드
const loadPost = async () => {
  try {
    const id = route.params.id;
    const token = localStorage.getItem('token');
    const response = await fetch(`http://127.0.0.1:8000/api/posts/${id}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`, // 토큰 추가
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    post.value = data;

    isAuthor.value = post.value.author === currentUser.value;  // 작성자 확인

    // 사용자가 이미 좋아요를 눌렀는지 확인
    isLiked.value = data.liked_users.includes(currentUser.value);
    console.log(data.liked_users);
    console.log(currentUser.value);
    console.log(isLiked.value);

  } catch (error) {
    console.error('게시글을 불러오는 중 오류가 발생했습니다:', error);
  }
};

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
    currentUser.value = data.username;  // 로그인된 사용자 정보 저장
    loadPost();  // 사용자 정보를 불러온 후 게시글을 로드

  } catch (error) {
    console.error('사용자 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 게시글 삭제 함수
const deletePost = async () => {
  try {
    const id = route.params.id;
    const token = localStorage.getItem('token');
    const response = await fetch(`http://127.0.0.1:8000/api/posts/${id}/delete/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`, // 토큰 추가
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    router.push('/posts'); // 삭제 후 게시판으로 리다이렉트
  } catch (error) {
    console.error('게시글 삭제 중 오류가 발생했습니다:', error);
  }
};

// 게시글 수정 페이지로 이동
const editPost = () => {
  router.push(`/posts/${post.value.id}/edit`); // 수정 페이지로 이동
};

const toggleLike = async () => {
  try {
    const id = route.params.id;
    const response = await fetch(`http://127.0.0.1:8000/api/posts/${id}/like/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    const result = await response.json();
    if (response.ok) {
      isLiked.value = !isLiked.value; // 좋아요 상태 토글
      post.value.likes += isLiked.value ? 1 : -1; // 좋아요 수 업데이트
    } else {
      console.error(result);
    }
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

const handleImageError = (event) => {
  console.log("Image failed to load:", event.target.src);  // 이미지 URL 출력
  event.target.src = '/static/images/default-user.png';   // 이미지가 없을 경우 기본 이미지로 대체
};

// 컴포넌트가 마운트되면 게시글 로드
onMounted(() => {
  loadCurrentUser();  // 로그인된 사용자 정보 로드
});
</script>

<style scoped>
/* 컨테이너 스타일 */
.post-detail-container {
  width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 제목 스타일 */
.post-title {
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 20px;
  text-align: center;
}

/* 내용 스타일 */
.post-content {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 20px;
  text-align: justify;
}

/* 메타 정보 */
.post-meta {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.post-author {
  font-weight: bold;
  color: #397edb;
}

.post-likes {
  font-weight: bold;
  color: #e38e49;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* 버튼 사이 간격 설정 */
  margin-bottom: 20px;
}


.like-button,
.delete-button,
.edit-button {
  padding: 10px 15px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* 좋아요 버튼 */
.like-button {
  background-color: #e38e49;
  color: white;
}

.like-button:hover {
  background-color: #ff7043;
}

/* 삭제 버튼 */
.delete-button {
  background-color: #dc3545;
  color: white;
}

.delete-button:hover {
  background-color: #c82333;
}

/* 수정 버튼 */
.edit-button {
  background-color: #007bff;
  color: white;
}

.edit-button:hover {
  background-color: #0056b3;
}

/* 뒤로가기 링크 */
.back-link {
  display: block;
  text-align: center;
  font-size: 1rem;
  color: #004aad;
  margin-top: 20px;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

/* 프로필 사진 */
.author-profile-pic {
  width: 30px;
  height: 30px;
  border-radius: 50%; /* 원형 */
  object-fit: cover; /* 비율 유지 및 잘림 */
  margin-right: 8px; /* 텍스트와 간격 */
  vertical-align: middle; /* 텍스트와 정렬 */
}
</style>
