<template>
  <header>
    <Navbar />
  </header>
  <div class="post-create-container">
    <h1 class="page-title">글 작성하기</h1>
    <form @submit.prevent="createPost" class="post-form">
      <div class="form-group">
        <label for="title" class="form-label">제목</label>
        <input
          id="title"
          v-model="title"
          class="form-input"
          placeholder="제목을 입력하세요"
          required
        />
      </div>
      <div class="form-group">
        <label for="content" class="form-label">내용</label>
        <textarea
          id="content"
          v-model="content"
          class="form-textarea"
          placeholder="내용을 입력하세요"
          required
        ></textarea>
      </div>
      <button type="submit" class="submit-button">작성하기</button>
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
    const response = await fetch(`${process.env.VITE_API_BASE_URL}api/posts/create/`, {
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
/* 페이지 컨테이너 스타일 */
.post-create-container {
  width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 제목 스타일 */
.page-title {
  text-align: center;
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 30px;
}

/* 폼 스타일 */
.post-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 폼 그룹 */
.form-group {
  display: flex;
  flex-direction: column;
}

/* 라벨 스타일 */
.form-label {
  font-size: 1rem;
  font-weight: bold;
  color: #555;
  margin-bottom: 8px;
}

/* 입력 필드 스타일 */
.form-input,
.form-textarea {
  width: 100%;
  padding: 15px;
  font-size: 1rem;
  border: 1px solid #d0d7e6;
  border-radius: 8px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s;
}

.form-input:focus,
.form-textarea:focus {
  border-color: #004aad;
  outline: none;
}

/* 텍스트 에어리어 */
.form-textarea {
  min-height: 150px;
  resize: none;
}

/* 제출 버튼 */
.submit-button {
  padding: 12px;
  background-color: #004aad;
  color: #fff;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #00337c;
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .post-create-container {
    padding: 20px;
  }

  .form-input,
  .form-textarea {
    padding: 10px;
  }

  .submit-button {
    font-size: 0.9rem;
  }
}
</style>
