<script setup>
import Navbar from "./Navbar.vue";

const isLogged = false;
const userName = "";
</script>

<template>
    <Navbar :is-logged="isLogged" :user-name="userName"/>
    <router-view/>
</template>