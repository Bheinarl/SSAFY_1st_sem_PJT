<template>
  <header> <Navbar /> </header>
  <div>
    <div class="leaderboard-container">
    <div class="leaderboard-header">
      <h1>🏆TOP 10🏆</h1>
      <h6 id="notice">Nickname 미설정 시 Username으로 기록됩니다!</h6>
    </div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else class="leaderboard">
      <div class="leaderboard-background">
        <table class="leaderboard-table">
          <thead>
            <tr>
              <th class="rank-column">Rank</th>
              <th class="user-column">User</th>
              <th class="score-column">Score</th>
            </tr>
          </thead>
          <tbody>
            <!-- 강조 조건 추가 -->
            <tr
              v-for="(user, index) in leaderboard"
              :key="user.username"
              :class="{ 'first-place': index === 0 }"
            >
              <td class="rank-column">{{ index + 1 }}</td>
              <td class="user-column">{{ user.nickname || user.username }}</td>
              <td class="score-column">{{ user.max_score }}</td>
            </tr>
          </tbody>
        </table>
      </div>
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
/* 1위 강조 스타일 */
.first-place {
  background-color: #fcd666 !important; /* 밝은 노란색 배경 */
  color: #004aad !important; /* 강조된 파란 글씨 */
  font-weight: bold; /* 텍스트 굵게 */
}

/* 마우스를 올렸을 때 강조 효과 */
.first-place:hover {
  background-color: #ffe082 !important; /* 밝은 노란색 강조 */
  transform: scale(1.05); /* 살짝 커지는 효과 */
  transition: all 0.2s ease-in-out;
}
/* 전체 컨테이너 스타일 */
.leaderboard-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 30px;
  background-color: #f9fbff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  color: #333;
}

/* 헤더 스타일 */
.leaderboard-header {
  text-align: center;
  margin-bottom: 20px;
}

.leaderboard-header h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  margin-bottom: 10px;
}

.leaderboard-header h6 {
  font-size: 0.9rem;
  color: #e38e49;
  font-weight: bold;
}

/* 순위표 테이블 */
.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
  background-color: #ffffff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.leaderboard-table th {
  background-color: #004aad;
  color: #ffffff;
  padding: 15px;
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.leaderboard-table td {
  padding: 15px;
  font-size: 1rem;
  color: #333;
  border-bottom: 1px solid #d0d7e6;
}

.leaderboard-table tr:nth-child(odd) {
  background-color: #f4f9ff;
}

.leaderboard-table tr:nth-child(even) {
  background-color: #ffffff;
}

.leaderboard-table tr:hover {
  background-color: #e4f1ff; /* 호버 효과 */
}

/* Rank 컬럼 스타일 */
.rank-column {
  font-weight: bold;
  color: #e38e49;
}

.user-column,
.score-column {
  color: #004aad;
}

/* 로딩 텍스트 */
.loading {
  text-align: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: #004aad;
}



</style>