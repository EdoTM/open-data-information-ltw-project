import { createApp } from "vue";
import App from "./App.vue";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import { createRouter, createWebHistory } from "vue-router";
import Home from "./components/Home.vue";
import Signup from "./components/Signup.vue";
import Report from "./components/Report.vue";

let router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: Home,
    },
    {
      path: "/signup",
      component: Signup,
    },
    {
      path: "/report",
      component: Report
    }
  ],
});

createApp(App).use(router).mount("#app");
