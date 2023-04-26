<script setup lang="ts">
const emits = defineEmits(["log-out", "toggle-theme"]);

function deleteCookie(name) {
  document.cookie = `${name}=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
}

function handleToggleTheme() {
  emits("toggle-theme");
}

function handleLogout() {
  deleteCookie("sessionID");
  emits("log-out");
  console.log("Logout successful");
}
</script>

<template>
  <nav class="navbar navbar-expand-sm bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">Navbar</a>
      <button
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
        class="navbar-toggler"
        data-bs-target="#navbarSupportedContent"
        data-bs-toggle="collapse"
        type="button"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div id="navbarSupportedContent" class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link aria-current="page" class="nav-link" to="/"
              >Plot
            </router-link>
          </li>
        </ul>
        <span class="nav-item me-2">
          <button
            class="btn btn-outline-secondary"
            href="#"
            @click="handleToggleTheme()"
          >
            <i
              v-if="theme === 'dark'"
              class="bi bi-sun-fill"
              style="font-size: 1em"
            ></i>
            <i v-else class="bi bi-moon-stars-fill"></i>
          </button>
        </span>
        <div v-if="!isLogged" class="navbar-nav">
          <a
            class="nav-link me-2"
            data-bs-target="#loginModal"
            data-bs-toggle="modal"
            href="#"
          >
            Log in
          </a>
          <router-link aria-current="page" class="btn btn-success" to="/signup"
            >Sign up
          </router-link>
        </div>
        <ul v-else class="navbar-nav">
          <li class="navbar-text me-3">Logged in as {{ userName }}</li>
          <li class="nav-item">
            <button
              aria-current="page"
              class="btn btn-outline-secondary"
              href="#"
              @click="handleLogout()"
            >
              Log out
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import Login from "./Login.vue";

export default {
  name: "Navbar",
  components: { Login },
  props: {
    isLogged: {
      type: Boolean,
      required: true,
    },
    userName: {
      type: String,
    },
    theme: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped></style>
