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
                <div v-if="isLogged === false" class="navbar-nav">
                    <a href="#" class="nav-link me-2" data-bs-toggle="modal" data-bs-target="#exampleModal">
                        Log in
                    </a>
                    <router-link class="btn btn-success" aria-current="page" to="/login">Sign up</router-link>
                </div>
                <ul v-else class="navbar-nav">
                    <li class="navbar-text me-3">
                        Logged in as {{ userName }}
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-secondary" aria-current="page" @click="isLogged = false;" href="#">Log out</button>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Log in</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <Login/>
                </div>
            </div>
        </div>
    </div>
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