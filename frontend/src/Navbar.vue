<script setup>

import {ref} from "vue";

const html = document.querySelector('html');
const themeInitial = html.getAttribute('data-bs-theme');
const theme = ref(themeInitial);

const emits = defineEmits(["log-out"]);


function toggleTheme() {
    if (theme.value === 'dark') {
        theme.value = 'light';
    } else {
        theme.value = 'dark';
    }
        html.setAttribute('data-bs-theme', theme.value);
}


function deleteCookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
function handleLogout() {
    deleteCookie("sessionID");
    emits("log-out");
    console.log("Logout successful");
}


</script>

<template>
    <nav class="navbar navbar-expand-sm bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                    data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                    aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" aria-current="page" to="/">Plot</router-link>
                    </li>
                </ul>
                <span class="nav-item me-2">
                    <button class="btn btn-outline-secondary" @click="toggleTheme()" href="#">
                        <i v-if="theme === 'dark'" class="bi bi-sun-fill" style="font-size: 1em"></i>
                        <i v-else class="bi bi-moon-stars-fill"></i>
                    </button>
                </span>
                <div v-if="isLogged === false" class="navbar-nav">
                    <a href="#" class="nav-link me-2" data-bs-toggle="modal" data-bs-target="#loginModal">
                        Log in
                    </a>
                    <router-link class="btn btn-success" aria-current="page" to="/signup">Sign up</router-link>
                </div>
                <ul v-else class="navbar-nav">
                    <li class="navbar-text me-3">
                        Logged in as {{ userName }}
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-secondary" aria-current="page" @click="handleLogout('sessionID');" href="#">Log out</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
import Login from "./Login.vue";

export default {
    name: "Navbar",
    components: {Login},
    props: {
        isLogged: {
            type: Boolean,
            required: true
        },
        userName: {
            type: String,
        }
    }
}
</script>

<style scoped>

</style>