<template>
  <div>
    <h1>Leaderboard</h1>
    <div v-if="loading">Loading...</div>
    <div v-else class="leaderboard">
      <div v-for="user in leaderboard" :key="user.username">
        <p class="rank">{{ user.username }} : {{ user.max_score }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

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
</style>