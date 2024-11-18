<template>
    <div>
        <h2>Your Profile</h2>
        <p><strong>Username:</strong> {{ profile.username }}</p>
        <p><strong>Nickname:</strong> {{ profile.nickname }}</p>
        <p><strong>Age:</strong> {{ profile.age }}</p>
        <p><strong>Interests:</strong> {{ profile.interests }}</p>
    </div>
</template>

<script>
import api from '../api';

export default {
    data() {
        return {
            profile: {}  // 사용자 프로필 데이터를 저장할 객체
        };
    },
    methods: {
        async fetchProfile() {
            try {
                const response = await api.get('/api/auth/user/');
                this.profile = response.data;  // 프로필 데이터를 Vue 데이터에 저장
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

<style scoped>
/* 필요한 경우 스타일 추가 */
</style>
