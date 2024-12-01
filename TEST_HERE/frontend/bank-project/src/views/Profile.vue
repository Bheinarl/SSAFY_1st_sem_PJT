<template>
  <header><Navbar /></header>
  <div class="profile">
    <div class="background-shapes">
      <div class="circle-large"></div>
      <div class="circle-medium"></div>
      <div class="circle-small"></div>
      <div class="rectangle"></div>
      <div class="triangle"></div>
      <div class="ellipse"></div>
    </div>
    <h1>User Profile</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <!-- Editing Form -->
      <div v-if="isEditing" class="form-container">
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="nickname">Nickname:</label>
            <input type="text" v-model="profile.nickname" id="nickname" maxlength="25"/>
          </div>
          <div class="form-group">
            <label for="age">Age:</label>
            <input type="number" v-model="profile.age" id="age" />
          </div>
          <div class="form-group">
            <label for="max_score">Max Score:</label>
            <input type="number" v-model="profile.max_score" id="max_score" disabled />
          </div>
          <div class="button-group">
            <button type="submit" class="btn save">Save Changes</button>
            <button type="button" @click="cancelEdit" class="btn cancel">Cancel</button>
          </div>
        </form>
      </div>
      <!-- Profile Details -->
      <div v-else class="profile-details">
        <div class="detail-row">
          <span class="label">Username:</span>
          <span class="value">{{ profile.username }}</span>
        </div>
        <div class="detail-row">
          <span class="label">Nickname:</span>
          <span class="value" v-if="profile.nickname">{{ profile.nickname }}</span>
          <span class="value" v-else>-</span>
        </div>
        <div class="detail-row">
          <span class="label">Age:</span>
          <span class="value" v-if="profile.age">{{ profile.age }}</span>
          <span class="value" v-else>-</span>
        </div>
        <div class="detail-row">
          <span class="label">My investor type:</span>
          <span class="highlight1" v-if="profile.my_investor_type">
            {{ profile.my_investor_type }}
            <!-- 😌🧐😏🤑 -->
            <span v-if="profile.my_investor_type ==='안정 추구형'">😌</span>
            <span v-if="profile.my_investor_type ==='균형 투자형'">🧐</span>
            <span v-if="profile.my_investor_type ==='공격 투자형'">😏</span>
            <span v-if="profile.my_investor_type ==='투기형'">🤑</span>
          </span>
          <span class="highlight2" v-else> GAME을 통해 확인하세요! </span>
        </div>
        <div class="detail-row">
          <span class="label">Max Score:</span>
          <span class="value">{{ profile.max_score }}</span>
        </div>
        <button @click="enableEdit" class="btn edit">Edit Profile</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import Navbar from '@/components/Navbar.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const profile = ref({
  username: '',
  nickname: '',
  age: '',
  my_investor_type: '',
  max_score: 0,
});

const loading = ref(true);
const isEditing = ref(false);

const fetchProfile = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    profile.value = response.data;
  } catch (error) {
    console.error('Failed to fetch profile:', error);
    alert('Failed to load profile.');
  } finally {
    loading.value = false;
  }
};

const updateProfile = async () => {
  try {
    await axios.patch('http://127.0.0.1:8000/accounts/update_profile/', profile.value, {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    alert('Profile updated successfully!');
    isEditing.value = false;
  } catch (error) {
    // 에러 메시지를 처리
    if (error.response && error.response.data) {
      // 닉네임 중복 에러 처리
      if (error.response.data.nickname) {
        alert(error.response.data.nickname[0]); // 서버로부터 오는 에러 메시지 표시
      } else {
        alert('Failed to update profile. Please try again.');
      }
    } else {
      console.error('Failed to update profile:', error);
      alert('An unexpected error occurred.');
    }
  }
};

const cancelEdit = () => {
  isEditing.value = false;
  fetchProfile();
};

const enableEdit = () => {
  isEditing.value = true;
};

onMounted(fetchProfile);
</script>

<style scoped>
.highlight1 {
  font-weight: bold;
}

.highlight2 {
  color: #e34949;
  font-weight: bold;
}

.profile {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #1F509A; /* 배경색 */
  color: #fff; /* 텍스트 색상 */
  text-align: center;
  font-family: 'Arial', sans-serif;
  height: calc(100vh - 55px); /* Navbar 높이를 뺀 값 */
  overflow: hidden; /* 강제로 스크롤 제거 */
}

h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #D4EBF8; /* 제목 텍스트 색상 */
}

.form-container,
.profile-details {
  z-index: 1; /* 도형보다 위에 표시 */
  background-color: #ffffff; /* 카드 배경 흰색 */
  color: #000000; /* 텍스트 색상 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 박스 그림자 */
  width: 450px;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 내부 요소 간격 */
}

.form-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px; /* 레이블과 입력 필드 간격 */
  margin : 15px;
}

.form-group label {
  flex: 1; /* 레이블 비율 */
  text-align: left;
  font-weight: bold;
  color: #1F509A; /* 레이블 텍스트 색상 */
  white-space: nowrap; /* 줄바꿈 방지 */
}

.form-group input {
  flex: 2; /* 입력 필드 비율 */
  padding: 8px;
  border: 1px solid #D4EBF8; /* 테두리 색상 */
  border-radius: 5px;
  background-color: #FEF9F6; /* 입력 필드 배경색 */
  outline: none;
  max-width: 100%; /* 필드 너비 제한 */
  box-sizing: border-box; /* 패딩 포함 크기 계산 */
}

.form-group input:focus {
  border-color: #E38E49; /* 포커스 상태 테두리 색상 */
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.detail-row .label {
  font-weight: bold;
  color: #1F509A; /* 상세 보기 레이블 색상 */
}

.detail-row .value {
  text-align: right;
  color: #333333; /* 상세 보기 값 색상 */
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px; /* 버튼 간격 */
}

.btn {
  flex: 1; /* 버튼 균등 너비 */
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn.save {
  background-color: #E38E49; /* 저장 버튼 색상 */
  color: #ffffff;
}

.btn.save:hover {
  background-color: #D4EBF8; /* 저장 버튼 호버 색상 */
  color: #1F509A; /* 텍스트 색상 */
}

.btn.cancel {
  background-color: #D4EBF8; /* 취소 버튼 색상 */
  color: #1F509A;
}

.btn.cancel:hover {
  background-color: #E38E49; /* 취소 버튼 호버 색상 */
  color: #ffffff;
}

.btn.edit {
  margin-top: 20px;
  background-color: #E38E49; /* 프로필 수정 버튼 색상 */
  color: #ffffff;
  align-self: center;
  width: 100%; /* 버튼 전체 너비 */
  text-align: center;
}



</style>
