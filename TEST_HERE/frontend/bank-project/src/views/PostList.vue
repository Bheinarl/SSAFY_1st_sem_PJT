<template>
  <div>
    <h1>게시판</h1>
    <ul v-if="posts.length">
      <li v-for="post in posts" :key="post.id">
        <router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link>
      </li>
    </ul>
    <p v-else>게시글이 없습니다.</p>
  </div>
</template>
  
  
<script setup>
import { ref, onMounted } from 'vue';

const posts = ref([]);

// 게시글 로드 함수
const loadPosts = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/posts/', {
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    posts.value = data;
  } catch (error) {
    console.error('게시글을 불러오는 중 오류가 발생했습니다:', error);
  }
};

// 컴포넌트가 마운트되면 게시글 로드
onMounted(loadPosts);
</script>