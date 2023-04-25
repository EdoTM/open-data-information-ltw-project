<script setup>
import axiosInstance from "./axiosInstance";
import md5 from "crypto-js/md5";

function generatePasswordMD5(plainPassword) {
    return md5(plainPassword).toString()
}

let loginError = "";

const sendLoginRequest = () => {
    const plainPassword = document.getElementById("inputPassword").value;

    axiosInstance.post("/login", {
        email: document.getElementById("inputEmail").value,
        password: generatePasswordMD5(plainPassword)
    }).then(response => {

        console.log(response);
    }).catch(error => {
        if (error.response.status === 401) {
            loginError = "INVALID_CREDENTIALS";
            console.log("LoginError: ", loginError);
        } else if (error.response.status === 404) {
            loginError = "USER_NOT_FOUND";
            console.log("LoginError: ", loginError);
        }
        else {
            loginError = "UNKNOWN_ERROR";
            console.log("error: ", error.response);
        }
    });
    console.log("loginError: ", loginError);
}
</script>

<template>
    <div class="mx-auto mb-4" style="max-width: 300px">
        <form @submit.prevent="sendLoginRequest">
            <div class="mb-3">
                <label for="inputEmail" class="form-label">Email address</label>
                <input type="email" class="form-control" id="inputEmail" required>
            </div>
            <div class="mb-3">
                <label for="inputPassword" class="form-label">Password</label>
                <input type="password" class="form-control" id="inputPassword" minlength="8" required>
            </div>
            <div class="alert alert-danger" role="alert">
                <span v-if="loginError === 'INVALID_CREDENTIALS'">Invalid password.</span>
                <span v-else-if="loginError === 'USER_NOT_FOUND'">User not found.</span>
            </div>
            <button type="submit" class="btn btn-primary mt-2">Login</button>
        </form>
    </div>

</template>

<script>

export default {
    name: "Login"
}
</script>
