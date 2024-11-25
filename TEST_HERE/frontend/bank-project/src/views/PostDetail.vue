<template>
  <div>
    <h1>{{ post.title }}</h1>
    <p>{{ post.content }}</p>
    <p>작성자: {{ post.author }}</p>
    <!-- <p>좋아요: {{ post.likes }}</p> -->
    <!-- <button @click="likePost">좋아요</button> -->
    <!-- 작성자와 현재 사용자 일치 시에만 표시 -->
    <button v-if="isAuthor" @click="deletePost">삭제</button>
    <button v-if="isAuthor" @click="editPost">수정</button>

    <router-link to="/posts">뒤로가기</router-link>
  </div>
</template>

<script>
import apiClient from '@/api';

export default {
  data() {
    return {
      post: {},
      currentUser: localStorage.getItem('username'), // 현재 사용자
    };
  },
  computed: {
    isAuthor() {
      return this.post.author === this.currentUser; // 작성자 확인
    },
  },
  async created() {
    const id = this.$route.params.id;
    const response = await apiClient.get(`/api/posts/${id}/`);
    this.post = response.data;
  },
  methods: {
    async deletePost() {
      const id = this.$route.params.id;
      await apiClient.delete(`/api/posts/${id}/`);
      this.$router.push('/posts'); // 삭제 후 게시판으로 리다이렉트
    },
    editPost() {
      this.$router.push(`/posts/${this.post.id}/edit`); // 수정 페이지로 이동
    },
    
    async likePost() {
      const id = this.$route.params.id;
      await apiClient.post(`/api/posts/${id}/like/`); // 좋아요 API 호출
      this.post.likes += 1; // 좋아요 수 업데이트
    },

  },
};
</script>
