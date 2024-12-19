import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia'; // Pinia 가져오기
import 'bootstrap/dist/css/bootstrap.min.css';
import './assets/styles/global.css';


const app = createApp(App);
const pinia = createPinia(); // Pinia 인스턴스 생성

app.use(pinia); // Pinia를 Vue 애플리케이션에 등록
app.use(router);
app.mount('#app');
