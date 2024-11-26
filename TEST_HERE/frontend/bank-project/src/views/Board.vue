<template>
  <header> <Navbar /> </header>
  <div>
    <h1>게시판</h1>
    <router-link to="/posts/new">글 작성하기</router-link>
    <ul v-if="posts.length > 0">
      <li v-for="post in posts" :key="post.id">
        <router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link>
        <span> | 작성자: {{ post.author }} | 좋아요: {{ post.likes }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Navbar from '@/components/Navbar.vue';

// Reactive state
const posts = ref([]);

// 게시글 불러오기
const fetchPosts = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/posts/list/');
    if (response.ok) {
      posts.value = await response.json();
    } else {
      console.error('Error fetching posts:', response.statusText);
    }
  } catch (error) {
    console.error('Error fetching posts:', error);
  }
};

// 컴포넌트가 마운트될 때 게시글을 가져옴
onMounted(() => {
  fetchPosts();
});
</script>
