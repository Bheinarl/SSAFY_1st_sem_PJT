<template>
  <header> <Navbar /> </header>
  <div>
    <div class="leaderboard-header">
      <h1>Leaderboard</h1>
      <h6 id="notice">nickname 미설정 시 username으로 기록</h6>
    </div>
    <div v-if="loading">Loading...</div>
    <div v-else class="leaderboard">
      <div v-for="user in leaderboard" :key="user.username">
        <p class="rank" v-if="user.max_score">
          {{ user.nickname || user.username }} : {{ user.max_score }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import Navbar from '@/components/Navbar.vue';
const leaderboard = ref([]);
const loading = ref(true);

const fetchLeaderboard = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/accounts/leaderboard/', {
      headers: {
        Authorization: `Token ${localStorage.getItem('token')}`,
      },
    });
    leaderboard.value = response.data;
  } catch (error) {
    console.error('Error fetching leaderboard:', error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchLeaderboard);
</script>

<style scoped>

.leaderboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.leaderboard {
  counter-reset: rank;
}

.rank {
  counter-increment: rank;
  font-size: 20px;
  margin-bottom: 10px;
}

.rank::before {
  content: counter(rank) ". ";
  font-weight: bold;
}

#notice {
  font-size: 15px;
  color: gray;
}
</style>