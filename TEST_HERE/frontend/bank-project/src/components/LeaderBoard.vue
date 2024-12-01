<template>
  <header>
    <Navbar />
  </header>
  <div class="leaderboard-container">
    <div class="leaderboard-header">
      <h1>🏆 랭킹 보드 🏆</h1>
      <h6 id="notice">초기 Nickname 미설정 시 Username으로 기록됩니다!</h6>
    </div>

    <!-- 상위 3명 -->
    <div class="top-three-section">
      <div class="top-three">
        <div
          v-for="(user, index) in topThree"
          :key="user.username"
          :class="['top-card', { 'gold': index === 0, 'silver': index === 1, 'bronze': index === 2 }]"
        >
          <div class="rank-icon">
            <span v-if="index === 0">🥇</span>
            <span v-else-if="index === 1">🥈</span>
            <span v-else>🥉</span>
          </div>
          <!-- 프로필 사진 출력 -->
          <img 
            :src="user.profile_picture.startsWith('/media/media/') 
                  ? `http://127.0.0.1:8000${user.profile_picture}` 
                  : 'http://127.0.0.1:8000/static/images/default-user.png'" 
            alt="User Avatar" 
            class="avatar" 
          />

<!-- 
          if not user.profile_picture:
        profile_data['profile_picture'] = f"http://127.0.0.1:8000/static/images/default-user.png"
    elif user.profile_picture.url.startswith('/media/'):
        profile_data['profile_picture'] = f"http://127.0.0.1:8000{user.profile_picture.url}" -->



          <h3>{{ user.nickname || user.username }}</h3>
          <p class="score">{{ user.max_score.toLocaleString() }}</p>
        </div>
      </div>
    </div>
  

    <!-- 랭킹 리스트 -->
    <div v-if="loading" class="loading">로딩 중...</div>
    <div v-else class="leaderboard">
      <table class="leaderboard-table">
        <thead>
          <tr>
            <th class="rank-column">Rank</th>
            <th class="user-column">User</th>
            <th class="score-column">Score</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(user, index) in paginatedLeaderboard"
            :key="user.username"
            :class="{ 'highlight-my-row': user.username === profile.username }"
          >
            <td class="rank-column">
              {{ index + 1 + (pagination.now_page_no - 1) * pagination.items_per_page }}
            </td>
            <td class="user-column">{{ user.nickname || user.username }}</td>
            <td class="score-column">{{ user.max_score }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 페이지네이션 -->
    <div class="pagination" v-if="pagination.total_count > 0">
      <button
        @click="changePage(pagination.now_page_no - 1)"
        :disabled="pagination.now_page_no === 1"
        class="pagination-btn"
      >
        이전
      </button>
      <span class="pagination-info">{{ pagination.now_page_no }} / {{ pagination.max_page_no }}</span>
      <button
        @click="changePage(pagination.now_page_no + 1)"
        :disabled="pagination.now_page_no === pagination.max_page_no"
        class="pagination-btn"
      >
        다음
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import Navbar from "@/components/Navbar.vue";

// 랭킹 데이터
const leaderboard = ref([
  // { username: "user1", nickname: "정글의실력있는투자자", max_score: 23124550745, profile_image: null },
  // { username: "user2", nickname: "바닷가의현명한BTC", max_score: 21127651264, profile_image: null },
  // { username: "user3", nickname: "목장의초명한이더리움", max_score: 19458660153, profile_image: null },
]);

const loading = ref(true);
const profile = ref({ max_score: 0, username: "" });
const myRank = ref(null);

const topThree = computed(() =>
  leaderboard.value
  .filter((user) => user.max_score > 0)
  .slice(0, 3)
  
);

const pagination = ref({
  total_count: 0,
  max_page_no: 1,
  now_page_no: 1,
  items_per_page: 5,
});

const paginatedLeaderboard = computed(() => {
  const filteredLeaderboard = leaderboard.value.filter((user) => user.max_score > 0);
  const start = (pagination.value.now_page_no - 1) * pagination.value.items_per_page;
  const end = start + pagination.value.items_per_page;
  return filteredLeaderboard.slice(start, end);
});

const fetchLeaderboard = async () => {
  console.log(leaderboard.value)
  try {
    const leaderboardResponse = await axios.get("http://127.0.0.1:8000/accounts/leaderboard/", {
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });
    leaderboard.value = leaderboardResponse.data || [];
    pagination.value.total_count = leaderboard.value.filter((user) => user.max_score > 0).length;
    pagination.value.max_page_no = Math.ceil(
      pagination.value.total_count / pagination.value.items_per_page
    );

    const profileResponse = await axios.get("http://127.0.0.1:8000/accounts/profile/", {
      headers: {
        Authorization: `Token ${localStorage.getItem("token")}`,
      },
    });
    profile.value = profileResponse.data;

    const rankIndex = leaderboard.value
      .filter((user) => user.max_score > 0)
      .findIndex((user) => user.username === profile.value.username);
    myRank.value = rankIndex !== -1 ? rankIndex + 1 : null;
  } catch (error) {
    console.error("데이터 로딩 오류:", error);
  } finally {
    loading.value = false;
  }
};

const changePage = (pageNo) => {
  if (pageNo < 1 || pageNo > pagination.value.max_page_no) return;
  pagination.value.now_page_no = pageNo;
};

onMounted(fetchLeaderboard);
</script>

<style scoped>
/* 컨테이너 */
.leaderboard-container {
  padding: 20px;
  max-width: 900px;
  margin: auto;
  background-color: #f4f9ff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-family: "Arial", sans-serif;
}

/* 헤더 */
.leaderboard-header h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  text-align: center;
  margin-bottom: 15px;
}

.leaderboard-header h6 {
  text-align: center;
  font-size: 0.9rem;
  color: #e38e49;
}

/* 상위 3명 섹션 */
.top-three-section {
  margin-bottom: 30px;
}

.top-three {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.top-card {
  background-color: #ffffff;
  border-radius: 10px;
  text-align: center;
  padding: 20px;
  width: 200px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease-in-out;
}

.top-card:hover {
  transform: scale(1.05);
}

/* 각 순위별 배경색 */
.top-card.gold {
  background: linear-gradient(145deg, #ffea92, #ffd700);
}

.top-card.silver {
  background: linear-gradient(145deg, #e0e0e0, #c0c0c0);
}

.top-card.bronze {
  background: linear-gradient(145deg, #d7a681, #cd7f32);
}

/* 순위 아이콘 */
.rank-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

/* 사용자 아바타 */
.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin: 10px auto;
  display: block;
}

/* 사용자 이름 */
h3 {
  font-size: 1.2rem;
  color: #004aad;
  margin: 10px 0;
}

/* 점수 */
.score {
  font-size: 1rem;
  font-weight: bold;
  color: #e38e49;
}


/* 컨테이너 */
.leaderboard-container {
  padding: 20px;
  max-width: 900px;
  margin: 20px auto;
  background-color: #f4f9ff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-family: "Arial", sans-serif;
}

/* 헤더 */
.leaderboard-header h1 {
  font-size: 2rem;
  font-weight: bold;
  color: #004aad;
  text-align: center;
  margin-bottom: 15px;
}

.leaderboard-header h6 {
  text-align: center;
  font-size: 0.9rem;
  color: #e38e49;
}

/* 상위 3명 */
.top-three-section {
  background-color: #f0f4ff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.top-three-section ul {
  list-style: none;
  padding: 0;
}

.top-three-section li {
  font-size: 1rem;
  margin: 5px 0;
  color: #333;
}

.top-rank {
  font-weight: bold;
  color: #e38e49;
}

/* 표 */
.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
}

.leaderboard-table th {
  background-color: #004aad;
  color: white;
  padding: 10px;
}

.leaderboard-table td {
  text-align: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

/* 내 순위 강조 */
.highlight-my-row {
  background-color: #ffe082;
  color: #004aad;
  font-weight: bold;
}

/* 페이지네이션 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 15px;
  background-color: #004aad;
  color: white;
  border: none;
  border-radius: 5px;
  margin: 0 5px;
  cursor: pointer;
  font-size: 1rem;
}

.pagination-btn:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 1rem;
  font-weight: bold;
  color: #333;
}
</style>
