<template>
  <div>
    <h1>게시판</h1>
    <router-link v-if="isAuthenticated" to="/posts/new">글 작성하기</router-link>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link>
        <span> | 작성자: {{ post.author }} | 좋아요: {{ post.likes }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  data() {
    return {
      posts: [],
      isAuthenticated: !!localStorage.getItem('token'),
    };
  },
  async created() {
    const response = await apiClient.get('/api/posts/');
    this.posts = response.data;
  },
};
</script>
