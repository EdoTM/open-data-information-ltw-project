<script setup>
import Navbar from "./Navbar.vue";
import Login from "./Login.vue";
import { onBeforeMount, ref } from "vue";
import { Modal } from "bootstrap";
import axiosInstance from "./axiosInstance";
import { getCookie, setCookie } from "./cookieUtils";

onBeforeMount(updateUserInfoIfCookiePresent);

function toggleTheme() {
    theme.value = theme.value === "dark" ? "light" : "dark";
    html.setAttribute("data-bs-theme", theme.value);
    setCookie("theme", theme.value);
}


const themeInitial = getCookie("theme") || "light";
const theme = ref(themeInitial);
const html = document.querySelector("html");
html.setAttribute("data-bs-theme", theme.value);

function updateUserInfoIfCookiePresent() {
  const sessionID = getCookie("sessionID")

  if (sessionID) {
    axiosInstance.get(`/userInfo?sessionID=${sessionID}`).then((response) => {
      const json = response.data;
      isLogged.value = true;
      setUserName(json.username);
      userEmail.value = json.email;
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
  Modal.getInstance(document.getElementById("loginModal")).hide();
}
</script>

<template>
  <Navbar
    :is-logged="isLogged"
    :user-name="userName"
    @log-out="isLogged = false"
    :theme="theme"
    @toggle-theme="toggleTheme"
  />

  <!-- Modal -->
  <div
    class="modal fade"
    id="loginModal"
    tabindex="-1"
    aria-labelledby="loginModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="loginModalLabel">Log in</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
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
    <router-view />
  </div>
</template>
