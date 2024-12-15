<template>
  <header> <Navbar /> </header>
  <div class="edit-container">
    <h1 class="title">게시글 수정</h1>
    <form @submit.prevent="updatePost" class="edit-form">
      <div class="form-group">
        <label for="title">제목</label>
        <input
          id="title"
          v-model="title"
          required
          class="form-input"
          placeholder="제목을 입력하세요"
        />
      </div>
      <div class="form-group">
        <label for="content">내용</label>
        <textarea
          id="content"
          v-model="content"
          required
          class="form-textarea"
          placeholder="내용을 입력하세요"
        ></textarea>
      </div>
      <button type="submit" class="btn-submit">수정하기</button>
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

<style scoped>
/* 컨테이너 스타일 */
.edit-container {
  width: 800px;
  margin: 30px auto;
  padding: 20px;
  background: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 제목 스타일 */
.title {
  font-size: 1.8rem;
  font-weight: bold;
  text-align: center;
  color: #004aad;
  margin-bottom: 20px;
}

/* 폼 그룹 스타일 */
.form-group {
  margin-bottom: 20px;
}

/* 폼 레이블 */
label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
  color: #333;
}

/* 폼 입력 스타일 */
.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-input:focus {
  outline: none;
  border-color: #004aad;
  box-shadow: 0 0 4px rgba(0, 74, 173, 0.3);
}

/* 텍스트 영역 스타일 */
.form-textarea {
  width: 100%;
  height: 120px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  resize: vertical;
}

.form-textarea:focus {
  outline: none;
  border-color: #004aad;
  box-shadow: 0 0 4px rgba(0, 74, 173, 0.3);
}

/* 제출 버튼 스타일 */
.btn-submit {
  width: 100%;
  padding: 12px 0;
  font-size: 1rem;
  font-weight: bold;
  color: white;
  background-color: #004aad;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-submit:hover {
  background-color: #002f6c;
}
</style>