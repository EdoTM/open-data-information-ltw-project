<script setup lang="ts">
import Navbar from "./components/TheNavbar.vue";
import Login from "./components/LoginForm.vue";
import { onBeforeMount, ref } from "vue";
import { Modal } from "bootstrap";
import axiosInstance from "./utils/axiosInstance";
import { getCookie } from "./utils/cookieUtils";

onBeforeMount(updateUserInfoIfCookiePresent);

const themeInitial = localStorage.getItem("theme") || "light";
const theme = ref(themeInitial);
const html = document.querySelector("html");
html.setAttribute("data-bs-theme", theme.value);

function toggleTheme() {
  theme.value = theme.value === "dark" ? "light" : "dark";
  html.setAttribute("data-bs-theme", theme.value);
  localStorage.setItem("theme", theme.value);
}

function updateUserInfoIfCookiePresent() {
  const sessionID = getCookie("sessionID");

  if (sessionID) {
    axiosInstance
      .get(`/userInfo?sessionID=${sessionID}`)
      .then((response) => {
        const json = response.data;
        isLogged.value = true;
        setUserName(json.username);
        userEmail.value = json.email;
      })
      .catch((error) => {
        if (error.response.status === 404) {
          console.log("Session ID not found");
        } else {
          console.log(error);
        }
      });
  }
}

function setUserName(name) {
  userName.value = `@${name}`;
}

const isLogged = ref(false);
const userName = ref("");
const userEmail = ref("");

function handleLogin() {
  isLogged.value = true;
  Modal.getInstance(document.getElementById("loginModal"))!.hide();
}
</script>

<template>
  <Navbar
    :is-logged="isLogged"
    :theme="theme"
    :user-name="userName"
    @log-out="isLogged = false"
    @toggle-theme="toggleTheme"
  />

  <!-- Modal -->
  <div
    id="loginModal"
    aria-hidden="true"
    aria-labelledby="loginModalLabel"
    class="modal fade"
    tabindex="-1"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 id="loginModalLabel" class="modal-title fs-5">Log in</h1>
          <button
            aria-label="Close"
            class="btn-close"
            data-bs-dismiss="modal"
            type="button"
          ></button>
        </div>
        <div class="modal-body">
          <Login
            @logged-in="handleLogin()"
            @update:user-email="userEmail = $event"
            @update:user-name="setUserName($event)"
          />
        </div>
      </div>
    </div>
  </div>

  <div class="m-5">
    <router-view :is-logged="isLogged" />
  </div>
</template>
