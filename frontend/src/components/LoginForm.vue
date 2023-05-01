<script setup lang="ts">
import axiosInstance from "../utils/axiosInstance";
import md5 from "crypto-js/md5";
import { ref } from "vue";
import { getInputElementById } from "../utils/tsUtils";
import { GoogleLogin } from "vue3-google-login";
import { sendGoogleSignInRequest } from "../utils/appUtils";

function generatePasswordMD5(plainPassword) {
  return md5(plainPassword).toString();
}

const loginError = ref("");

const emits = defineEmits([
  "logged-in",
  "update:user-name",
  "update:user-email",
  "update:user-picture",
]);

function handleLoginResponse(response) {
  const json = response.data as UserInfoResponse;
  emits("logged-in", true);
  emits("update:user-name", json.username);
  emits("update:user-email", json.email);
  emits("update:user-picture", json.profilePic);
  console.log("Login successful");
}

function loginFromFields() {
  const plainPassword = getInputElementById("inputPassword").value;

  const login = {
    email: getInputElementById("inputEmail").value,
    password: generatePasswordMD5(plainPassword),
  };

  console.log(login);

  axiosInstance
    .post("/login", login)
    .then(handleLoginResponse)
    .catch((error) => {
      console.log(error);
      if (error.response.status === 401) {
        loginError.value = "INVALID_CREDENTIALS";
      } else if (error.response.status === 404) {
        loginError.value = "USER_NOT_FOUND";
      }
      console.log("LoginError: ", loginError);
    });
}
</script>

<template>
  <div class="mx-auto mb-4" style="max-width: 300px">
    <form @submit.prevent="loginFromFields">
      <div class="form-floating mb-3">
        <input
          id="inputEmail"
          class="form-control"
          placeholder="Email"
          required
          type="email"
        />
        <label for="inputEmail">Email address</label>
      </div>
      <div class="form-floating mb-3">
        <input
          id="inputPassword"
          class="form-control"
          minlength="8"
          placeholder="Password"
          required
          type="password"
        />
        <label for="inputPassword">Password</label>
      </div>
      <div
        v-if="loginError === 'INVALID_CREDENTIALS'"
        class="alert alert-danger"
        role="alert"
      >
        Invalid password.
      </div>
      <div
        v-else-if="loginError === 'USER_NOT_FOUND'"
        class="alert alert-danger"
        role="alert"
      >
        User not found.
      </div>
      <div
        v-else-if="loginError === 'UNKNOWN_ERROR'"
        class="alert alert-danger"
        role="alert"
      >
        An error occurred.
      </div>
      <div class="mx-auto d-flex mt-3" style="color-scheme: light !important">
        <button class="btn btn-primary" style="float: left" type="submit">
          Login
        </button>
        <div class="flex-grow-1 text-center my-auto">or</div>
        <GoogleLogin
          :callback="
            (r) => sendGoogleSignInRequest(r).then(handleLoginResponse)
          "
          :button-config="{
            locale: 'en',
            text: 'signin_with',
            width: '20',
          }"
        />
      </div>
    </form>
  </div>
</template>
