<script setup>
import Navbar from "./Navbar.vue";

const isLogged = false;
const userName = "";
</script>

<template>
    <Navbar :is-logged="isLogged" :user-name="userName"/>
    <div class="m-5">
        <router-view/>
    </div>
</template>