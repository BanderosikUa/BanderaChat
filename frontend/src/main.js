import { createApp } from "vue";

import PerfectScrollbar from 'vue3-perfect-scrollbar'

import 'vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css'
import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap";
import './interceptors/axios'

import App from './App.vue';
import router from './router';

const app = createApp(App);

app.use(router);
app.use(PerfectScrollbar)
app.mount("#app");
