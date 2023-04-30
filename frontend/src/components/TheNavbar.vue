<script setup lang="ts">
import { deleteCookie } from "../utils/cookieUtils";
import { breakpointsBootstrapV5, useBreakpoints } from "@vueuse/core";

defineProps<{
  isLogged: boolean;
  theme: string;
  userName?: string;
}>();

const navbarBreakpoint = "sm";

const breakpoints = useBreakpoints(breakpointsBootstrapV5);
const isDesktop = breakpoints.greater(navbarBreakpoint);

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
            <router-link aria-current="page" class="nav-link" to="/">
              Home
            </router-link>
          </li>
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
          <span class="navbar-text me-3">Logged in as {{ userName }}</span>
          <button
            aria-current="page"
            class="btn btn-outline-secondary"
            href="#"
            @click="handleLogout()"
          >
            Log out
          </button>
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