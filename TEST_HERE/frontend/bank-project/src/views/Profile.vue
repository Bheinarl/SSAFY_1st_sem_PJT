<template>
  <div>
    <h1>User Profile</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-if="isEditing">
        <form @submit.prevent="updateProfile">
          <div>
            <label for="nickname">Nickname</label>
            <input type="text" v-model="profile.nickname" id="nickname" />
          </div>
          <div>
            <label for="age">Age</label>
            <input type="number" v-model="profile.age" id="age" />
          </div>
          <div>
            <label for="interests">Interests</label>
            <textarea v-model="profile.interests" id="interests"></textarea>
          </div>
          <div>
            <label for="max_score">Max Score</label>
            <input type="number" v-model="profile.max_score" id="max_score" disabled />
          </div>
          <button type="submit">Save Changes</button>
          <button type="button" @click="cancelEdit">Cancel</button>
        </form>
      </div>
      <div v-else>
        <p><strong>Nickname:</strong> {{ profile.nickname }}</p>
        <p><strong>Age:</strong> {{ profile.age }}</p>
        <p><strong>Interests:</strong> {{ profile.interests }}</p>
        <p><strong>Max Score:</strong> {{ profile.max_score }}</p>
        <button @click="enableEdit">Edit Profile</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 프로필 데이터 초기화
const profile = ref({
  nickname: '',
  age: '',
  interests: '',
  max_score: 0,
});

const loading = ref(true);
const isEditing = ref(false); // 수정 모드 상태

// 로그인한 사용자 정보 가져오기
const fetchProfile = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/profile/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    profile.value = response.data; // 응답 데이터로 프로필 업데이트
  } catch (error) {
    console.error('Failed to fetch profile:', error);
  } finally {
    loading.value = false; // 로딩 완료
  }
};

// 프로필 수정 처리
const updateProfile = async () => {
  try {
    const response = await axios.patch(
      'http://127.0.0.1:8000/accounts/update_profile/',
      profile.value, // 변경된 프로필 데이터 전송
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      }
    );
    alert('Profile updated successfully!');
    isEditing.value = false; // 수정 모드 종료
  } catch (error) {
    console.error('Failed to update profile:', error);
  }
};

// 수정 취소 처리
const cancelEdit = () => {
  isEditing.value = false; // 수정 모드 종료
  fetchProfile(); // 수정 취소 시 원래 값으로 되돌리기
};

// 수정 모드 활성화
const enableEdit = () => {
  isEditing.value = true; // 수정 모드 활성화
};

// 컴포넌트가 마운트될 때 프로필 데이터 가져오기
onMounted(fetchProfile);
</script>

<style scoped>

</style>