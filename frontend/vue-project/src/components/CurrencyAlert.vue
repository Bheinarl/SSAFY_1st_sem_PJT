<template>
  <div>
    <h3>해외 소비를 위한 환율 알림</h3>
    <form @submit.prevent="setAlert">
      <input v-model="currency" placeholder="통화(예: USD)" />
      <input v-model="targetRate" type="number" placeholder="목표 환율" />
      <button type="submit">알림 설정</button>
    </form>
    <p v-if="alertSet">환율 알림이 설정되었습니다!</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currency: '',
      targetRate: '',
      alertSet: false,
    };
  },
  methods: {
    async setAlert() {
      try {
        const response = await fetch("http://127.0.0.1:8000/accounts/set_alert/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            currency: this.currency,   // 사용자가 입력한 통화 정보
            target_rate: this.targetRate,  // 사용자가 입력한 목표 환율
          }),
        });
        const data = await response.json();
        if (data.status === 'success') {
          alert("목표 환율이 설정되었습니다.");
        }
      } catch (error) {
        console.error("목표 환율 설정 중 오류가 발생했습니다.", error);
      }
    },
  },
};
</script>
