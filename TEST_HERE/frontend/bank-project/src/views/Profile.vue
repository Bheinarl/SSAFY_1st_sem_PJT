<template>
  <div class="profile-container">
    <h1 class="title">User Profile</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <div v-if="isEditing" class="form-container">
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="nickname">Nickname</label>
            <input type="text" v-model="profile.nickname" id="nickname" />
          </div>
          <div class="form-group">
            <label for="age">Age</label>
            <input type="number" v-model="profile.age" id="age" />
          </div>
          <div class="form-group">
            <label for="interests">Interests</label>
            <textarea v-model="profile.interests" id="interests"></textarea>
          </div>
          <div class="form-group">
            <label for="max_score">Max Score</label>
            <input type="number" v-model="profile.max_score" id="max_score" disabled />
          </div>
          <div class="button-group">
            <button type="submit" class="btn save">Save Changes</button>
            <button type="button" @click="cancelEdit" class="btn cancel">Cancel</button>
          </div>
        </form>
      </div>
      <div v-else class="profile-details">
        <p><strong>Username:</strong> {{ profile.username }}</p>
        <p><strong>Nickname:</strong> {{ profile.nickname }}</p>
        <p><strong>Age:</strong> {{ profile.age }}</p>
        <p><strong>My investor type:</strong> {{ profile.my_investor_type }}</p>
        <p><strong>Max Score:</strong> {{ profile.max_score }}</p>
        <button @click="enableEdit" class="btn edit">Edit Profile</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const profile = ref({
  username: '',
  nickname: '',
  age: '',
  interests: '',
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
  } finally {
    loading.value = false;
  }
};

const updateProfile = async () => {
  try {
    const response = await axios.patch(
      'http://127.0.0.1:8000/accounts/update_profile/',
      profile.value,
      {
        headers: {
          Authorization: `Token ${localStorage.getItem('token')}`,
        },
      }
    );
    alert('Profile updated successfully!');
    isEditing.value = false;
  } catch (error) {
    console.error('Failed to update profile:', error);
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
.profile-container {
  background-color: #fff4f1; /* 배경 색상 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  color: #ee6463;
  font-weight: bold;
}

.profile-details,
.form-container {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

input,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ffa29c;
  border-radius: 5px;
  background-color: #feebd6;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #ee6463;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.btn.save {
  background-color: #ee6463;
  color: white;
}

.btn.cancel {
  background-color: #ffa29c;
  color: black;
}

.btn.edit {
  background-color: #ffa29c;
  color: black;
}
.template {
  background-color: #ffa29c;
}
</style>
