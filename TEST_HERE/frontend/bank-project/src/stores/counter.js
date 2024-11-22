import axios from 'axios';
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', () => {
  const register = async (payload) => {
    try {
      const { username, password1, password2, email } = payload;
      const response = await axios.post('http://127.0.0.1:8000/api/auth/registration/', {
        username,
        password1,
        password2,
        email,
      });
      console.log('회원가입 성공:', response.data);
      return response.data;
    } catch (error) {
      console.error('회원가입 실패:', error.response?.data || error);
      throw error;
    }
  };

  const login = async (credentials) => {
    try {
      const { username, password } = credentials;
      const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
        username,
        password,
      });
      console.log('로그인 성공:', response.data);
      return response.data;
    } catch (error) {
      console.error('로그인 실패:', error.response?.data || error);
      throw error;
    }
  };

  return { register, login };
});