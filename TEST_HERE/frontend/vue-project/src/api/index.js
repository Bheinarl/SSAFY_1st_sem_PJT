import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    withCredentials: true,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token'); // 로그인 시 저장된 JWT 토큰을 가져옴
    if (token) {
        config.headers.Authorization = `Token ${token}`; // Authorization 헤더에 토큰 추가
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;
