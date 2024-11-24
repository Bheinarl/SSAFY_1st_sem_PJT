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
  
  
  <script>
  import apiClient from '@/api';
  
  export default {
    data() {
      return {
        posts: [],
      };
    },
    async created() {
      const response = await apiClient.get('/posts/');
      this.posts = response.data;
    },
  };
  </script>
  