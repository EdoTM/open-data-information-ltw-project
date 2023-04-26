<script setup>
import axiosInstance from "./axiosInstance";
import md5 from "crypto-js/md5";
import {onMounted, ref} from "vue";

function generatePasswordMD5(plainPassword) {
  return md5(plainPassword).toString();
}

const signupError = ref("");

const emits = defineEmits([
  "logged-in",
  "update:user-name",
  "update:user-email",
]);

function handleResponse(response) {
  // TODO: Handle response, this is just the login response handling
  const json = response.data;
  emits("logged-in", true);
  emits("update:user-name", json.username);
  emits("update:user-email", json.email);
  console.log("Login successful");
}

function sendSignUpRequest() {
  const plainPassword = document.getElementById("signupInputPassword").value;

  const signup = {
    email: document.getElementById("signupInputEmail").value,
    password: generatePasswordMD5(plainPassword),
    username: document.getElementById("signupInputUsername").value,
    birthdate: document.getElementById("signupInputBirthdate").value,
  };

  console.log(signup);

  axiosInstance
    .post("/signup", signup)
    .then(handleResponse)
    .catch((error) => {
      console.log(error);
      if (error.response.status === 409) {
        // if ("Username" in error.response.data.error) 
        if (error.response.data.error.includes("Username")) {
          signupError.value = "Username already taken";
        } else if (error.response.data.error.includes("Email")) {
          signupError.value = "Email already taken";
        }
      }
      console.log("LoginError: ", signupError);
    });
}

function checkSignUpFormValidity() {
  const form = document.getElementById("form-coso");
  form.addEventListener(
    "submit",
    (event) => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      } else {
          sendSignUpRequest();
      }
      form.classList.add("was-validated");

    },
    false
  );
}

onMounted(() => {
  checkSignUpFormValidity();
});
</script>

<template>
  <div class="mx-auto mb-4" style="max-width: 300px">
    <h1>Sign up</h1>
    <form novalidate id="form-coso" @submit.prevent="() => {}">
      <div class="form-floating mb-3">
        <input
          type="email"
          class="form-control"
          id="signupInputEmail"
          required
          placeholder="s"
          pattern="[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[a-z]+$"
        />
        <div class="invalid-feedback">Insert a valid email address.</div>
        <label for="signupInputEmail">Email address</label>
      </div>
      <div class="input-group mb-3 has-validation">
        <span class="input-group-text">@</span>
        <div class="form-floating">
          <input
            type="text"
            class="form-control"
            id="signupInputUsername"
            placeholder="Username"
            required
            pattern="[A-Za-z0-9_-]{1,15}$"
            maxlength="15"
          />
          <label for="signupInputUsername">Username</label>
        </div>
        <div class="invalid-feedback">Username is not valid.</div>
      </div>
      <div class="form-floating mb-3">
        <input
          type="password"
          class="form-control"
          id="signupInputPassword"
          placeholder="Password"
          minlength="8"
          required
        />
        <label for="signupInputPassword">Password</label>
        <div class="invalid-feedback">Insert a valid password.</div>
      </div>
      <div class="form-floating mb-3">
        <input
          type="password"
          class="form-control"
          id="signupInputRepeatPassword"
          required
          placeholder="s"
          minlength="8"
        />
        <label for="signupInputRepeatPassword">Repeat password</label>
        <div class="invalid-feedback">Insert a valid password</div>
      </div>
      <div class="form-floating mb-3">
        <input
          type="date"
          class="form-control"
          id="signupInputBirthdate"
          required
          placeholder="Birht date"
        />
        <label for="signupInputBirthdate">Birth date</label>
        <div class="invalid-feedback">Insert a valid birth date.</div>
      </div>
      <div class="form-check">
        <input
          class="form-check-input"
          type="checkbox"
          value=""
          id="invalidCheck"
          required
        />
        <label class="form-check-label" for="invalidCheck">
          Agree to terms and conditions
        </label>
        <div class="invalid-feedback">You must agree before submitting.</div>
      </div>
      <button
        type="submit"
        class="btn btn-success mt-2"
      >
        Sign up
      </button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Signup",
};
</script>