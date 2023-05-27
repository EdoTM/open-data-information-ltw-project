<script setup lang="ts">
import { deleteCookie } from "../utils/cookieUtils";
import { bs5Breakpoints } from "../utils/appUtils";
import { inject, Ref } from "vue";

defineProps<{
  theme: string;
  userName?: string;
  profilePic?: string;
}>();

const isLogged = inject<Ref<boolean>>("is-logged");

const navbarBreakpoint = "md";
const isDesktop = bs5Breakpoints.greater(navbarBreakpoint);

const emits = defineEmits(["log-out", "toggle-theme"]);

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
  <nav :class="`navbar navbar-expand-${navbarBreakpoint} bg-body-tertiary`">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Open data analysis</a>
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
            <router-link aria-current="page" class="nav-link" to="/plot">
              Plot
            </router-link>
          </li>
          <li class="nav-item">
            <router-link aria-current="page" class="nav-link" to="/report">
              Report
            </router-link>
          </li>
          <li class="nav-item">
            <router-link aria-current="page" class="nav-link" to="/searchUsers">
              Users
            </router-link>
          </li>
        </ul>
        <div v-if="!isLogged" class="navbar-nav">
          <a
            class="nav-link me-2"
            data-bs-target="#loginModal"
            data-bs-toggle="modal"
            href="#"
          >
            Log in
          </a>
          <router-link
            aria-current="page"
            :class="[
              isDesktop
                ? 'btn btn-success'
                : 'nav-link text-decoration-none text-success fw-bold',
            ]"
            to="/signup"
          >
            Sign up
          </router-link>
        </div>
        <div v-else class="navbar-nav">
          <span v-if="isDesktop" class="my-auto">
            <img alt="profilePic" class="profile-pic" :src="profilePic" />
          </span>
          <div class="nav-item dropdown me-2">
            <a
              aria-expanded="false"
              class="nav-link dropdown-toggle"
              data-bs-toggle="dropdown"
              href="#"
              role="button"
            >
              {{ userName }}
            </a>
            <ul class="dropdown-menu">
              <li>
                <a
                  :href="'/profile?username=' + userName"
                  class="dropdown-item"
                >
                  <i class="bi-person-fill me-2" />
                  Profile
                </a>
              </li>
              <li>
                <hr class="dropdown-divider" />
              </li>
              <li>
                <a class="dropdown-item" href="/favorites">
                  <i class="bi-star-fill me-2" />
                  Favorite posts
                </a>
              </li>
              <li>
                <a class="dropdown-item" href="/hidden">
                  <i class="bi-eye-slash-fill me-2" />
                  Hidden posts
                </a>
              </li>
            </ul>
          </div>
          <a
            aria-current="page"
            :class="[
              isDesktop
                ? 'btn btn-outline-secondary'
                : 'nav-link text-decoration-none text-danger fw-bold',
            ]"
            href="#"
            @click="handleLogout()"
          >
            Log out
          </a>
        </div>
        <div class="navbar-nav">
          <span class="nav-item">
            <button
              :class="[`btn btn-link nav-link ms-${navbarBreakpoint}-2`]"
              href="#"
              :style="['font-size: ' + (isDesktop ? '1.2rem' : '1em')]"
              @click="handleToggleTheme()"
            >
              <span v-if="!isDesktop"> Toggle theme </span>
              <i v-if="theme === 'dark'" class="bi bi-sun-fill"></i>
              <i v-else class="bi bi-moon-stars-fill"></i>
            </button>
          </span>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.profile-pic {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
}
</style>