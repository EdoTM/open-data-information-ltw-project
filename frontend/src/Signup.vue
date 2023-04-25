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
    const json = response.data;
    emits("logged-in", true);
    emits("update:user-name", json.username);
    emits("update:user-email", json.email);
    console.log("Login successful");
}

function sendLoginRequest() {
    const plainPassword = document.getElementById("inputPassword").value;

    const signup = {
        email: document.getElementById("inputEmail").value,
        password: generatePasswordMD5(plainPassword)
    }

    console.log(signup)

    axiosInstance.post("/signup", signup).then(handleResponse).catch(error => {
        console.log(error)
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
        <form @submit.prevent="sendLoginRequest">
            <div class="form-floating mb-3">
                <input type="email" class="form-control" id="inputEmail" required placeholder="s">
                <label for="inputEmail">Email address</label>
            </div>
            <div class="input-group mb-3">
                <span class="input-group-text">@</span>
                <div class="form-floating">
                    <input type="text" class="form-control" id="inputUsername" placeholder="Username" required>
                    <label for="inputUsername">Username</label>
                </div>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="inputPassword" required placeholder="s">
                <label for="inputPassword">Password</label>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="inputRepeatPassword" required placeholder="s">
                <label for="inputRepeatPassword">Repeat password</label>
            </div>
            <div class="form-floating mb-3">
                <input type="date" class="form-control" id="inputBirthdate" required placeholder="s">
                <label for="inputBirthdate">Birth date</label>
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