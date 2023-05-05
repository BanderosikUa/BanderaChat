import { createApp } from "vue";

import axios from 'axios';
// import io from 'socket.io-client'
import PerfectScrollbar from 'vue3-perfect-scrollbar'

import 'vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css'
import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap";

import App from './App.vue';
import router from './router';

const app = createApp(App);

// axios.defaults.withCredentials = true;
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*';
axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');
// axios.defaults.baseURL = 'http://34.120.190.133/';  // the FastAPI backend
axios.defaults.baseURL = 'http://127.0.0.1:5000/';  // the FastAPI backend
// io.defaults.baseURL = 'http://127.0.0.1:5000/' 

app.use(router);
app.use(PerfectScrollbar)
app.mount("#app");
