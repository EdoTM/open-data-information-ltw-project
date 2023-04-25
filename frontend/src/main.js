import { createApp } from 'vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.min.css'
import {createRouter, createWebHistory} from "vue-router";
import Home from "./Home.vue";
import Signup from "./Signup.vue";

let router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/signup',
            component: Signup
        }
    ]
});

createApp(App)
    .use(router)
    .mount('#app')
