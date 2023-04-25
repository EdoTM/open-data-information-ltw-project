<script setup>
import axios from "axios";
import md5 from "crypto-js/md5";

function generatePasswordMD5(plainPassword) {
    return md5(plainPassword).toString()
}

const sendLoginRequest = () => {
    const plainPassword = document.getElementById("inputPassword").value;

    axios.post("http://localhost:5000/signup", {
        email: document.getElementById("inputEmail").value,
        password: generatePasswordMD5(plainPassword),
        username: document.getElementById("inputUsername").value,
        birthday: document.getElementById("inputBirthday").value
    }).then(response => {
        console.log(response);
    }).catch(error => {
        console.log(error);
    });
}
</script>

<template>
    <div class="m-5 mx-auto" style="max-width: 300px">

    <form @submit.prevent="sendLoginRequest">
        <div class="mb-3">
            <label for="inputEmail" class="form-label">Email address</label>
            <input type="email" class="form-control" id="inputEmail" required>
        </div>
        <div class="mb-3">
            <label for="inputPassword" class="form-label">Password</label>
            <input type="password" class="form-control" id="inputPassword" minlength="8" required>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    </div>

</template>

<script>

export default {
    name: "Signup"
}
</script>
