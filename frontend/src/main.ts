import { createApp } from "vue";
import App from "./App.vue";
import vue3GoogleLogin from "vue3-google-login";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import SignupPage from "./pages/SignupPage.vue";
import ReportPage from "./pages/ReportPage.vue";
import PlotPage from "./pages/PlotPage.vue";

let router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: HomePage,
    },
    {
      path: "/signup",
      component: SignupPage,
    },
    {
      path: "/report",
      component: ReportPage,
    },
    {
      path: "/plot",
      component: PlotPage,
    },
  ],
});

createApp(App)
    .use(router)
    .use(vue3GoogleLogin, {
      clientId: "524814186523-b4scb23kumgek58om66nog5p6efr8l2t.apps.googleusercontent.com",
    })
    .mount("#app");
