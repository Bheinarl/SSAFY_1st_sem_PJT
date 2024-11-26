<template>
  <header> <Navbar /> </header>
  <div>
    <h1>게시글 수정</h1>
    <form @submit.prevent="updatePost">
      <div>
        <label for="title">제목</label>
        <input id="title" v-model="title" required />
      </div>
      <div>
        <label for="content">내용</label>
        <textarea id="content" v-model="content" required></textarea>
      </div>
      <button type="submit">수정하기</button>
    </form>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const title = ref('');
const content = ref('');
const postId = route.params.id;  // URL에서 게시글 ID를 가져옴

// 게시글 불러오기
const loadPost = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await fetch(`http://127.0.0.1:8000/api/posts/${postId}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
    });
    if (response.ok) {
      const data = await response.json();
      title.value = data.title;
      content.value = data.content;
    } else {
      console.error('게시글을 불러오는 중 오류가 발생했습니다:', response.statusText);
    }
  } catch (error) {
    console.error('게시글을 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 게시글 수정
const updatePost = async () => {
  try {
    const token = localStorage.getItem('token');
    const updatedPost = { title: title.value, content: content.value };
    
    const response = await fetch(`http://127.0.0.1:8000/api/posts/${postId}/edit/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
      body: JSON.stringify(updatedPost),
    });

    if (response.ok) {
      console.log('게시글 수정 성공');
      router.push(`/posts/${postId}`);  // 수정된 게시글 페이지로 이동
    } else {
      console.error('게시글 수정 실패:', response.statusText);
    }
  } catch (error) {
    console.error('게시글 수정 실패:', error);
  }
};

// 페이지 로드 시 게시글 정보 불러오기
onMounted(() => {
  loadPost();
});
</script>
