<script lang="ts" setup>
import { onBeforeMount, ref } from "vue";
import { AllUsersResponse } from "../types/apiTypes";
import axiosInstance from "../utils/axiosInstance";

const searchQuery = ref<string>("");
const users = ref<AllUsersResponse[]>([]);
const shownUsers = ref<AllUsersResponse[]>([]);

function handleQueryChange(newQuery: string) {
  searchQuery.value = newQuery;
  if (newQuery === "") {
    shownUsers.value = users.value;
  } else {
    shownUsers.value = users.value.filter((u) =>
      u.username.toLowerCase().includes(newQuery.toLowerCase())
    );
  }
}

function getAllUsers() {
  axiosInstance.get("/getAllUsers").then((response) => {
    users.value = response.data;
    shownUsers.value = users.value;
  });
}

onBeforeMount(getAllUsers);
</script>

<template>
  <div class="container d-flex flex-column">
    <h1 class="my-4 mx-auto text-center">Search users</h1>
    <div class="input-group mx-auto" style="max-width: 25rem">
      <span class="input-group-text"><i class="bi-search" /></span>
      <input
        :value="searchQuery"
        class="form-control"
        placeholder="Search users..."
        type="text"
        @input="handleQueryChange($event.target.value)"
      />
    </div>
    <div
      v-if="shownUsers.length !== 0"
      class="list-group my-5 mx-auto"
      style="max-width: max-content"
    >
      <a
        v-for="user in shownUsers"
        :href="`/profile?username=${user.username}`"
        aria-current="true"
        class="list-group-item list-group-item-action d-flex px-5 py-4"
      >
        <img :src="user.profile_pic" alt="" class="user-picture my-auto me-3" />
        <span class="my-auto display-6">@{{ user.username }}</span>
      </a>
    </div>
    <div v-else>
      <h2 class="display-6 text-center mt-5">
        No users matching '{{ searchQuery }}'
      </h2>
    </div>
  </div>
</template>

<style scoped>
.user-picture {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 10px;
}
</style>