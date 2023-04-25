<script setup>
import axiosInstance from "./axiosInstance";
import md5 from "crypto-js/md5";
import {ref} from "vue";

function generatePasswordMD5(plainPassword) {
    return md5(plainPassword).toString()
}

const loginError = ref("");

const emits = defineEmits(["logged-in", "update:user-name", "update:user-email"])

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
        birthdate: document.getElementById("signupInputBirthdate").value

    }

    console.log(signup)

    axiosInstance.post("/signup", signup).then(handleResponse).catch(error => {
        console.log(error)
        // TODO: Handle errors, this is just the login error handling
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
    <h1>Sign up</h1>
        <form @submit.prevent="sendSignUpRequest">
            <div class="form-floating mb-3">
                <input type="email" class="form-control" id="signupInputEmail" required placeholder="s">
                <label for="signupInputEmail">Email address</label>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">@</span>
                <div class="form-floating">
                    <input type="text" class="form-control" id="signupInputUsername" placeholder="Username" required>
                    <label for="signupInputUsername">Username</label>
                </div>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="signupInputPassword" required placeholder="s">
                <label for="signupInputPassword">Password</label>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="signupInputRepeatPassword" required placeholder="s">
                <label for="signupInputRepeatPassword">Repeat password</label>
            </div>
            <div class="form-floating mb-3">
                <input type="date" class="form-control" id="signupInputBirthdate" required placeholder="s">
                <label for="signupInputBirthdate">Birth date</label>
            </div>
            <button type="submit" class="btn btn-success mt-2">Sign up</button>
        </form>
    </div>

</template>

<script>
export default {
    name: "Login"
}
</script>