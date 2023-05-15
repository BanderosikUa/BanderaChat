import { createApp } from "vue";

import PerfectScrollbar from 'vue3-perfect-scrollbar'

import 'vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css'
import 'sweetalert2/dist/sweetalert2.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap";
import './interceptors/axios'

import App from './App.vue';
import router from './router';
import config from './config.js'

const app = createApp(App);

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives
})

app.config.globalProperties.$config = config

app.use(router);
app.use(PerfectScrollbar)
app.use(vuetify)
app.mount("#app");
