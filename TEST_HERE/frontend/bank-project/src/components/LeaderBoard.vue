<template>
  <header> <Navbar /> </header>
  <div>
    <div class="leaderboard-header">
      <h1>Leaderboard</h1>
      <h6 id="notice">nickname 미설정 시 username으로 기록</h6>
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
            <tr v-for="user in leaderboard" :key="user.username">
              <td class="rank-column">{{ leaderboard.indexOf(user) + 1 }}</td>
              <td class="user-column">{{ user.nickname || user.username }}</td>
              <td class="score-column">{{ user.max_score }}</td>
            </tr>
          </tbody>
        </table>
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
/* 전체 페이지 스타일 */
body {
  background-color: #1F509A; /* 배경 색상 */
  font-family: 'Arial', sans-serif;
  color: white;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* 순위표를 감싸는 컨테이너 */
.leaderboard-container {
  width: 90%;
  max-width: 1200px;
  background-color: white; /* 메모장 느낌의 배경 */
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

/* 헤더 스타일 */
.leaderboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  background-color: #1F509A;
}

.leaderboard-header h1 {
  margin: 0;
  font-size: 28px;
  font-weight: 600;
}

.leaderboard-header h6 {
  font-size: 14px;
  color: #E38E49;
  margin: 0;
  font-weight: 400;
}

/* 로딩 텍스트 */
.loading {
  color: #E38E49;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  padding: 20px;
}

/* 순위표 테이블 스타일 */
.leaderboard {
  padding: 20px 0;
}

.leaderboard-background {
  background-color: #F8F8F8; /* 메모장 느낌의 배경 */
  border-radius: 10px;
  padding: 20px;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #0A3981;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.leaderboard-table th,
.leaderboard-table td {
  padding: 12px 20px;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
}

.leaderboard-table th {
  background-color: #1F509A;
  color: #E38E49;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.leaderboard-table td {
  color: #D4EBF8;
  border-top: 1px solid #E38E49;
}

.leaderboard-table tr:hover {
  background-color: #0A3981; /* 호버 시 색상 변화 */
}

.leaderboard-table tr:nth-child(even) {
  background-color: #1F509A; /* 짝수 행 배경색 */
}

.leaderboard-table tr:nth-child(odd) {
  background-color: #0A3981; /* 홀수 행 배경색 */
}

.rank-column {
  font-size: 20px;
  color: #E38E49; /* 순위 강조 색상 */
}

.user-column {
  font-size: 18px;
}

.score-column {
  font-size: 18px;
}

/* 공지사항 스타일 */
#notice {
  font-size: 15px;
  color: gray;
  margin-top: 10px;
  text-align: center;
}
</style>