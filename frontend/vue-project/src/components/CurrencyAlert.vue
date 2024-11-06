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
        const response = await fetch('/accounts/set_alert/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            currency: this.currency,
            target_rate: this.targetRate,
          }),
        });
        if (response.ok) {
          this.alertSet = true;
        }
      } catch (error) {
        console.error('Error setting alert:', error);
      }
    },
  },
};
</script>
