import { createApp } from "vue";
import App from "./App.vue";
import vue3GoogleLogin from "vue3-google-login";

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import { createRouter, createWebHistory } from "vue-router";
import HomePage from "./pages/HomePage.vue";
import SignupPage from "./pages/SignupPage.vue";
import PlotPage from "./pages/PlotPage.vue";
import CommentsPage from "./pages/posts/CommentsPage.vue";
import FavoritePosts from "./pages/posts/FavoritePosts.vue";
import ReportPage from "./pages/posts/ReportPage.vue";
import HiddenPosts from "./pages/posts/HiddenPosts.vue";
import ProfilePage from "./pages/profile/ProfilePage.vue";
import ProfileNotExistsPage from "./pages/profile/ProfileNotExistsPage.vue";

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
    {
      path: "/favorites",
      component: FavoritePosts,
    },
    {
      path: "/hidden",
      component: HiddenPosts,
    },
    {
      path: "/comment",
      component: CommentsPage,
    },
    {
      path: "/profile",
      component: ProfilePage,
    },
    {
      path: "/profile404",
      component: ProfileNotExistsPage,
    },
  ],
});

createApp(App)
  .use(router)
  .use(vue3GoogleLogin, {
    clientId:
      "524814186523-b4scb23kumgek58om66nog5p6efr8l2t.apps.googleusercontent.com",
  })
  .mount("#app");
