<template>
    <div>
      <h1>글 작성하기</h1>
      <form @submit.prevent="createPost">
        <div>
          <label for="title">제목</label>
          <input id="title" v-model="form.title" required />
        </div>
        <div>
          <label for="content">내용</label>
          <textarea id="content" v-model="form.content" required></textarea>
        </div>
        <button type="submit">작성하기</button>
      </form>
    </div>
  </template>
  
  <script>
  import apiClient from '@/api';
  
  export default {
    data() {
      return {
        form: {
          title: '',
          content: '',
        },
      };
    },
    methods: {
      async createPost() {
        try {
          await apiClient.post('/api/posts/', this.form); // API에 데이터 전송
          this.$router.push('/posts'); // 글 작성 후 게시판 목록으로 이동
        } catch (error) {
          console.error('게시글 작성 중 오류:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  form {
    display: flex;
    flex-direction: column;
  }
  label {
    margin-bottom: 5px;
  }
  input, textarea {
    margin-bottom: 15px;
    padding: 10px;
    font-size: 16px;
  }
  button {
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  </style>
  