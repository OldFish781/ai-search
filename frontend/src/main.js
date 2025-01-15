import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import 'katex/dist/katex.min.css';
import '@/assets/css/style.css';

createApp(App).use(store).mount('#app');
