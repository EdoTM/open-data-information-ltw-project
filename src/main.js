import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import {createRouter, createWebHistory} from "vue-router";
import Home from "./Home.vue";
import Login from "./Login.vue";

let router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/login',
            component: Login
        }
    ]
});

createApp(App)
    .use(router)
    .mount('#app')
