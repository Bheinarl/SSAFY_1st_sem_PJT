<template>
  <header>
    <Navbar />
  </header>
  <div class="post-detail-container">
    <h1 class="post-title">{{ post.title }}</h1>
    <div class="post-meta">
      <div class="post-author">
        <img :src="post.author_profile_picture || '/default-user.png'" alt="Author's profile picture" class="author-profile-pic2" @error="handleImageError" />
        <span>작성자: {{ post.author }}</span>
      </div>
      <span class="post-likes">좋아요: {{ post.likes }}</span>
    </div>
    <p class="post-content">{{ post.content }}</p>

    <div class="button-group">
      <button @click="toggleLike" class="like-button">
        {{ isLiked ? '좋아요 취소' : '좋아요' }}
      </button>
      <button v-if="isAuthor"@click="editPost" class="edit-button">수정</button>
      <button v-if="isAuthor"@click="deletePost" class="delete-button">삭제</button>
    </div>

    <div class="comments-section">
      <h3>댓글</h3>
      <ul>
        <li v-for="comment in comments" :key="comment.id" class="comment-item">
          <img :src="comment.author_profile_picture || '/default-user.png'" alt="Author's profile picture" class="author-profile-pic2" @error="handleImageError" />
          <div class="comment-content">
            <p><strong>{{ comment.author }}</strong>: {{ comment.content }}</p>
          </div>

          <div v-if="comment.author === currentUser" class="comment-actions">
            <button @click="editComment(comment)" class="btn edit">수정</button>
            <button @click="deleteComment(comment.id)" class="btn delete">삭제</button>
          </div>
          <div v-if="editingComment === comment.id" class="comment-edit-form">
            <textarea v-model="editingContent" placeholder="댓글을 수정하세요"></textarea>
            <button @click="submitEditComment">수정 완료</button>
            <button @click="cancelEditComment">취소</button>
          </div>
        </li>
      </ul>
      

      <!-- 댓글 작성 폼 -->
      <div class="comment-form">
        <textarea v-model="newComment" placeholder="댓글을 입력하세요"></textarea>
        <button @click="submitComment(post.id)">댓글 작성</button>
      </div>
    </div>

    <router-link to="/posts" class="back-link">뒤로가기</router-link>
  </div>
</template>


<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios'

const route = useRoute();
const router = useRouter();

const post = ref({});
const currentUser = ref(localStorage.getItem('username')?.trim());

// 작성자 확인
const isAuthor = ref(false);
const isLiked = ref(false);

// 댓글
const comments = ref([]);
const newComment = ref('');

const editingComment = ref(null); // 현재 수정 중인 댓글 ID
const editingContent = ref('');   // 수정할 댓글 내용

// 데이터 로드
const loadPost = async () => {
  try {
    const id = route.params.id;
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.VITE_API_BASE_URL}api/posts/${id}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`, // 토큰 추가
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API 응답 데이터:', data);  // 디버깅용 출력
    post.value = data;

    if (currentUser.value && post.value.author) {
      isAuthor.value = post.value.author === currentUser.value;
      console.log('isAuthor:', isAuthor.value);
    }

    // 사용자가 이미 좋아요를 눌렀는지 확인
    isLiked.value = data.liked_users.includes(currentUser.value);
    console.log('data:', data.liked_users);
    console.log('currentUser', currentUser.value);
    console.log('isLiked', isLiked.value);

  } catch (error) {
    console.error('게시글을 불러오는 중 오류가 발생했습니다:', error);
  }
};

const loadCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    // 토큰이 없으면 로그인 페이지로 리다이렉트
    router.push('/login');
    return;
  }

  try {
    const response = await fetch(`${process.env.VITE_API_BASE_URL}accounts/get_current_user/`, {
      method: 'GET',
      headers: {
        Authorization: `Token ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('여기여기', data)
    currentUser.value = data.nickname ? data.nickname : data.username; // nickname이 존재하면 nickname, 없으면 username
    loadPost();  // 사용자 정보를 불러온 후 게시글을 로드

  } catch (error) {
    console.error('사용자 정보를 불러오는 중 오류가 발생했습니다:', error);
  }
};

const fetchComments = async (postId) => {
  try {
    const response = await axios.get(
      `${process.env.VITE_API_BASE_URL}api/posts/${postId}/comments/`,
      { headers: { Authorization: `Token ${localStorage.getItem('token')}` } }
    );
    comments.value = response.data;
  } catch (error) {
    console.error('Error fetching comments:', error);
  }
};

const submitComment = async (postId) => {
  try {
    const response = await axios.post(
      `${process.env.VITE_API_BASE_URL}api/posts/${postId}/comments/create/`,
      { content: newComment.value },
      { headers: { Authorization: `Token ${localStorage.getItem('token')}` } }
    );
    comments.value.push(response.data);
    newComment.value = '';
  } catch (error) {
    console.error('Error creating comment:', error);
  }
};

// 댓글 삭제 함수
const deleteComment = async (commentId) => {
  try {
    await axios.delete(`${process.env.VITE_API_BASE_URL}api/posts/${post.value.id}/comments/${commentId}/delete/`, {
      headers: { Authorization: `Token ${localStorage.getItem('token')}` },
    });
    comments.value = comments.value.filter(comment => comment.id !== commentId); // 삭제된 댓글 제외
    alert('댓글이 삭제되었습니다.');
  } catch (error) {
    console.error('Error deleting comment:', error.response?.data || error.message);
  }
};

// 댓글 수정 활성화
const editComment = (comment) => {
  console.log('Editing comment:', comment);
  editingComment.value = comment.id;
  editingContent.value = comment.content;
};

// 수정된 댓글 제출
const submitEditComment = async () => {
  try {
    const response = await axios.put(
      `${process.env.VITE_API_BASE_URL}api/posts/${post.value.id}/comments/${editingComment.value}/edit/`,
      { content: editingContent.value },
      { headers: { Authorization: `Token ${localStorage.getItem('token')}` } }
    );
    // 수정된 댓글 반영
    const updatedCommentIndex = comments.value.findIndex(comment => comment.id === editingComment.value);
    comments.value[updatedCommentIndex].content = response.data.content;
    alert('댓글이 수정되었습니다.');
    cancelEditComment();
  } catch (error) {
    console.error('Error editing comment:', error.response?.data || error.message);
  }
};

// 댓글 수정 취소
const cancelEditComment = () => {
  editingComment.value = null;
  editingContent.value = '';
};


// 게시글 삭제 함수
const deletePost = async () => {
  try {
    const id = route.params.id;
    const token = localStorage.getItem('token');
    const response = await fetch(`${process.env.VITE_API_BASE_URL}api/posts/${id}/delete/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`, // 토큰 추가
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    router.push('/posts'); // 삭제 후 게시판으로 리다이렉트
  } catch (error) {
    console.error('게시글 삭제 중 오류가 발생했습니다:', error);
  }
};

// 게시글 수정 페이지로 이동
const editPost = () => {
  router.push(`/posts/${post.value.id}/edit`); // 수정 페이지로 이동
};

const toggleLike = async () => {
  try {
    const id = route.params.id;
    const response = await fetch(`${process.env.VITE_API_BASE_URL}api/posts/${id}/like/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    const result = await response.json();
    if (response.ok) {
      isLiked.value = !isLiked.value; // 좋아요 상태 토글
      post.value.likes += isLiked.value ? 1 : -1; // 좋아요 수 업데이트
    } else {
      console.error('좋아요 오류', result);
    }
  } catch (error) {
    console.error('좋아요 처리 중 오류가 발생했습니다:', error);
  }
};

const handleImageError = (event) => {
  console.log("Image failed to load:", event.target.src);  // 이미지 URL 출력
  event.target.src = '/default-user.png';   // 이미지가 없을 경우 기본 이미지로 대체
};


// 컴포넌트가 마운트되면 게시글 로드
onMounted(async () => {
  await loadCurrentUser();  // currentUser를 먼저 로드
  await loadPost();         // 그 후 post 데이터를 불러옴
  fetchComments(route.params.id);  // 댓글 불러오기
});
</script>

<style scoped>
/* 컨테이너 스타일 */
.post-detail-container {
  width: 800px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  color: #333;
}

/* 제목 스타일 */
.post-title {
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 20px;
  text-align: center;
}

/* 내용 스타일 */
.post-content {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 20px;
  text-align: justify;
}

/* 메타 정보 */
.post-meta {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.post-author {
  font-weight: bold;
  color: #397edb;
}

.post-likes {
  font-weight: bold;
  color: #e38e49;
}

.button-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* 버튼 사이 간격 설정 */
  margin-bottom: 20px;
}


.like-button,
.delete-button,
.edit-button {
  padding: 10px 15px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* 좋아요 버튼 */
.like-button {
  background-color: #e38e49;
  color: white;
}

.like-button:hover {
  background-color: #ff7043;
}

/* 삭제 버튼 */
.delete-button {
  background-color: #dc3545;
  color: white;
}

.delete-button:hover {
  background-color: #c82333;
}

/* 수정 버튼 */
.edit-button {
  background-color: #007bff;
  color: white;
}

.edit-button:hover {
  background-color: #0056b3;
}

/* 뒤로가기 링크 */
.back-link {
  display: block;
  text-align: center;
  font-size: 1rem;
  color: #004aad;
  margin-top: 20px;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

/* 프로필 사진 */
.author-profile-pic2 {
  width: 30px;
  height: 30px;
  border-radius: 50%; /* 원형 */
  object-fit: cover; /* 비율 유지 및 잘림 */
  margin-right: 8px; /* 텍스트와 간격 */
  vertical-align: middle; /* 텍스트와 정렬 */
}

/* 댓글 */

.comments-section {
  margin-top: 20px;
}

.comments-section ul {
  list-style: none;
  padding: 0;
}

.comments-section li {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.comment-form textarea {
  width: 100%;
  height: 80px;
  margin-top: 10px;
  padding: 10px;
  box-sizing: border-box;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.comment-form button {
  margin-top: 10px;
  padding: 8px 15px;
  background-color: #004aad;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.comment-form button:hover {
  background-color: #00337c;
}


.comment-actions {
  display: flex;
  gap: 10px;
}

.comment-actions .btn {
  padding: 5px 10px;
  font-size: 0.9rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.comment-actions .edit {
  background-color: #ffc107;
  color: white;
}

.comment-actions .delete {
  background-color: #dc3545;
  color: white;
}

.comment-edit-form {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.comment-edit-form textarea {
  width: 100%;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ddd;
}

.comment-edit-form button {
  padding: 8px 10px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}

.comment-edit-form button:hover {
  background-color: #0056b3;
}
</style>
