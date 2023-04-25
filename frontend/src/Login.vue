<script setup>
import axios from "axios";
import md5 from "crypto-js/md5";

function generatePasswordMD5(plainPassword) {
    return md5(plainPassword).toString()
}

const sendLoginRequest = () => {
    const plainPassword = document.getElementById("inputPassword").value;

    axios.post("http://localhost:5000/login", {
        email: document.getElementById("inputEmail").value,
        password: generatePasswordMD5(plainPassword)
    }).then(response => {
        console.log(response);
    }).catch(error => {
        console.log(error);
    });
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
            <button type="submit" class="btn btn-primary mt-2">Submit</button>
        </form>
    </div>

</template>

<script>

export default {
    name: "Login"
}
</script>
