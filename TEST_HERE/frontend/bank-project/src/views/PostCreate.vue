<template>
  <header> <Navbar /> </header>
  <div>
    <h1>글 작성하기</h1>
    <form @submit.prevent="createPost">
      <div>
        <label for="title">제목</label>
        <input id="title" v-model="title" required />
      </div>
      <div>
        <label for="content">내용</label>
        <textarea id="content" v-model="content" required></textarea>
      </div>
      <button type="submit">작성하기</button>
    </form>
  </div>
</template>
  
<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const title = ref('')
const content = ref('')
const router = useRouter()

const createPost = async () => {
  try {
    const token = localStorage.getItem('token')
    const post = { title: title.value, content: content.value }
    console.log('글 작성 요청:', post)
    const response = await fetch('http://127.0.0.1:8000/api/posts/create/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Token ${token}` },
      
      body: JSON.stringify(post)
    });

    const result = await response.json()

    if (response.ok) {
      console.log('글 작성 성공', result)
      router.push('/posts')
    } else {
      console.error('글 작성 실패:', result)
    }
  } catch (error) {
    console.error('글 작성 실패:', error)
  } finally {
    title.value = ''
    content.value = ''
  }
}

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
  