<script setup>
import Navbar from "./Navbar.vue";
import Login from "./Login.vue";
import { ref } from "vue";
import { Modal } from "bootstrap";

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
            @update:user-name="userName = '@' + $event"
          />
        </div>
      </div>
    </div>
  </div>

  <div class="m-5">
    <router-view />
  </div>
</template>
