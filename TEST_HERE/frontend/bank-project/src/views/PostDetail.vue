<template>
  <header> <Navbar /> </header>
  <div>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p>작성자: {{ post.author }}</p>
    <p>좋아요: {{ post.likes }}</p>
    <button @click="toggleLike">{{ isLiked ? '좋아요 취소' : '좋아요' }}</button>
    
    <div v-if="isAuthor">  <!-- 작성자와 현재 사용자 일치 시에만 표시 -->
      <button @click="deletePost">삭제</button>
      <button @click="editPost">수정</button>
    </div>

    <router-link to="/posts">뒤로가기</router-link>
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

// 컴포넌트가 마운트되면 게시글 로드
onMounted(() => {
  loadCurrentUser();  // 로그인된 사용자 정보 로드
});
</script>