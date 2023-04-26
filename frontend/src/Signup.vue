<script setup>
import axiosInstance from "./axiosInstance";
import md5 from "crypto-js/md5";
import { onMounted, ref } from "vue";

const props = defineProps({
  isLogged: Boolean,
});

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
  const json = response.data;
  emits("logged-in", true);
  emits("update:user-name", json.username);
  emits("update:user-email", json.email);
  console.log("Login successful");
  window.location.href = "/";
}

const usernameTaken = ref(false);
const emailTaken = ref(false);

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
        usernameTaken.value = false;
        if (error.response.data.error.includes("Username")) {
          signupError.value = "Username already taken";
          document
            .getElementById("signupInputUsername")
            .setCustomValidity("Username already taken");
          usernameTaken.value = true;
        } else if (error.response.data.error.includes("Email")) {
          signupError.value = "Email already taken";
          document
            .getElementById("signupInputEmail")
            .setCustomValidity("Email already registered");
          emailTaken.value = true;
        }
      }
      console.log("LoginError: ", signupError);
    });
}

function resetUsernameValidity() {
  document.getElementById("signupInputUsername").setCustomValidity("");
  usernameTaken.value = false;
}

function resetEmailValidity() {
  document.getElementById("signupInputEmail").setCustomValidity("");
  emailTaken.value = false;
}

function addCheckPasswordMatchListener() {
  const password = document.getElementById("signupInputPassword");
  const passwordRepeat = document.getElementById("signupInputRepeatPassword");

  [passwordRepeat, password].map((p) =>
    p.addEventListener(
      "input",
      () => {
        if (password.value !== passwordRepeat.value) {
          passwordRepeat.setCustomValidity("Passwords don't match");
        } else {
          passwordRepeat.setCustomValidity("");
        }
      },
      false
    )
  );
}

function addCheckBirthdateEventListener() {
  const birthdate = document.getElementById("signupInputBirthdate");
  birthdate.addEventListener(
    "input",
    () => {
      const today = new Date();
      const birthdateDate = new Date(birthdate.value);
      if (birthdateDate > today || birthdateDate < new Date(1900, 0, 1)) {
        birthdate.setCustomValidity("Birthdate is not valid");
      } else {
        birthdate.setCustomValidity("");
      }
    },
    false
  );
}

function addCheckSignUpFormListener() {
  const form = document.getElementById("form-coso");
  form.addEventListener(
    "submit",
    (event) => {
      const isValid = form.checkValidity();
      if (!isValid) {
        event.preventDefault();
        event.stopPropagation();
      } else {
        sendSignUpRequest();
        window.location.href = "/";
      }
      form.classList.add("was-validated");
    },
    false
  );
}

onMounted(() => {
  addCheckSignUpFormListener();
  addCheckPasswordMatchListener();
  addCheckBirthdateEventListener();
});
</script>

<template>
  <div
    v-if="isLogged"
    class="d-flex justify-content-center flex-column mx-auto"
    style="width: 50%"
  >
    <h1 class="text-center mb-5">You are already logged in</h1>
    <img
      alt="You are already logged in"
      class="mx-auto"
      src="https://media.tenor.com/x8v1oNUOmg4AAAAd/rickroll-roll.gif"
      style="max-width: 400px"
    />
  </div>
  <div v-else class="mx-auto mb-4" style="max-width: 300px">
    <h1>Sign up</h1>
    <form id="form-coso" novalidate @submit.prevent="() => {}">
      <div :class="['form-floating mb-3' + (emailTaken ? ' is-invalid' : '')]">
        <input
          id="signupInputEmail"
          class="form-control"
          pattern="[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[a-z]+$"
          placeholder="Email"
          required
          type="email"
          @input="resetEmailValidity"
        />
        <div v-if="emailTaken" class="invalid-feedback">
          Email is already registered. Maybe you want to log in?
        </div>
        <div v-else class="invalid-feedback">Email is not valid.</div>
        <label for="signupInputEmail">Email address</label>
      </div>
      <div class="input-group mb-3 has-validation">
        <span class="input-group-text">@</span>
        <div :class="['form-floating' + (usernameTaken ? ' is-invalid' : '')]">
          <input
            id="signupInputUsername"
            class="form-control"
            maxlength="15"
            pattern="[A-Za-z0-9_-]{1,15}$"
            placeholder="Username"
            required
            type="text"
            @input="resetUsernameValidity"
          />
          <label for="signupInputUsername">Username</label>
        </div>
        <div v-if="usernameTaken" class="invalid-feedback">
          Username already taken.
        </div>
        <div v-else class="invalid-feedback">Username is not valid.</div>
      </div>
      <div class="form-floating mb-3">
        <input
          id="signupInputPassword"
          class="form-control"
          minlength="8"
          placeholder="Password"
          required
          type="password"
        />
        <label for="signupInputPassword">Password</label>
        <div class="invalid-feedback">Insert a valid password.</div>
      </div>
      <div class="form-floating mb-3">
        <input
          id="signupInputRepeatPassword"
          class="form-control"
          placeholder="Repeat password"
          required
          type="password"
        />
        <label for="signupInputRepeatPassword">Repeat password</label>
        <div class="invalid-feedback">Passwords don't match</div>
      </div>
      <div class="form-floating mb-3">
        <input
          id="signupInputBirthdate"
          class="form-control"
          placeholder="Birht date"
          required
          type="date"
        />
        <label for="signupInputBirthdate">Birth date</label>
        <div class="invalid-feedback">Insert a valid birth date.</div>
      </div>
      <div class="form-check">
        <input
          id="invalidCheck"
          class="form-check-input"
          required
          type="checkbox"
          value=""
        />
        <label class="form-check-label" for="invalidCheck">
          Agree to terms and conditions
        </label>
        <div class="invalid-feedback">You must agree before submitting.</div>
      </div>
      <button class="btn btn-success mt-2" type="submit">Sign up</button>
    </form>
  </div>
</template>

<script>
export default {
  name: "Signup",
};
</script>