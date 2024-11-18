<template>
  <div>
    <h2>주식 데이터</h2>
    <p>데이터 출력 {{ stocks }}</p>
  </div>
</template>

<script setup>
import api from '../api';

export default {
    data() {
        return {
            stocks: {}  // 사용자 프로필 데이터를 저장할 객체
        };
    },
    methods: {
        async fetchProfile() {
            try {
                const response = await api.get('/api/auth/user/');
                this.stocks = response.data;  // 프로필 데이터를 Vue 데이터에 저장
            } catch (error) {
                console.error('Error fetching profile data:', error);
                alert('Failed to load profile information. Please try again.');
            }
        }
    },
    created() {
        this.fetchProfile();  // 컴포넌트 생성 시 프로필 데이터를 불러옴
    }
};
</script>

<style lang="scss" scoped>

</style>