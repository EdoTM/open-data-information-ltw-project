<script setup lang="ts">
import { onMounted, ref } from "vue";
import { getInputElementById } from "../utils/tsUtils";
import {
  generatePasswordMD5,
  sendGoogleSignInRequest,
  sendSignUpRequest,
} from "../utils/appUtils";
import { AxiosResponse } from "axios";
import { SignInResponse, SignUpRequest } from "../types/apiTypes";

defineProps<{
  isLogged: boolean;
}>();

const emits = defineEmits([
  "logged-in",
  "update:user-name",
  "update:user-email",
]);

function handleSignupResponse(response: AxiosResponse<SignInResponse>) {
  const json = response.data;
  emits("logged-in", true);
  emits("update:user-name", json.username);
  emits("update:user-email", json.email);
  console.log("Login successful");
  window.location.href = "/";
}

const usernameTaken = ref(false);
const emailTaken = ref(false);

function signupFromFields() {
  const plainPassword = getInputElementById("signupInputPassword").value;

  const signup: SignUpRequest = {
    email: getInputElementById("signupInputEmail").value,
    password: generatePasswordMD5(plainPassword),
    username: getInputElementById("signupInputUsername").value,
    birthdate: getInputElementById("signupInputBirthdate").value,
  };

  sendSignUpRequest(signup)
    .then(handleSignupResponse)
    .catch((error) => {
      console.log(error);
      if (error.response.status === 409) {
        usernameTaken.value = false;
        if (error.response.data.error.includes("Username")) {
          getInputElementById("signupInputUsername").setCustomValidity(
            "Username already taken"
          );
          usernameTaken.value = true;
        } else if (error.response.data.error.includes("Email")) {
          getInputElementById("signupInputEmail").setCustomValidity(
            "Email already registered"
          );
          emailTaken.value = true;
        }
      }
    });
}

function resetUsernameValidity() {
  getInputElementById("signupInputUsername").setCustomValidity("");
  usernameTaken.value = false;
}

function resetEmailValidity() {
  getInputElementById("signupInputEmail").setCustomValidity("");
  emailTaken.value = false;
}

function addCheckPasswordMatchListener() {
  const password = getInputElementById("signupInputPassword");
  const passwordRepeat = getInputElementById("signupInputRepeatPassword");

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
  const birthdate = getInputElementById("signupInputBirthdate");
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
  const form = getInputElementById("form-coso");
  form.addEventListener(
    "submit",
    (event) => {
      const isValid = form.checkValidity();
      if (!isValid) {
        event.preventDefault();
        event.stopPropagation();
      } else {
        signupFromFields();
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
  <div v-else class="mx-auto mt-5" style="max-width: 300px">
    <h1 class="my-3 text-center">Sign up</h1>
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
      <button class="btn btn-success mt-3 w-100" type="submit">Sign up</button>
    </form>
    <div class="flex-grow-1 text-center my-2">or</div>
    <div style="width: 100%">
      <GoogleLogin
        :callback="(r) => sendGoogleSignInRequest(r).then(handleSignupResponse)"
        style="color-scheme: light"
        class="mx-auto"
        :button-config="{
          locale: 'en',
          text: 'signup_with',
          width: 300,
          shape: 'circle',
          theme: 'filled_blue',
        }"
      />
    </div>
  </div>
</template>