<script lang="ts" setup>
import { computed, inject, ref, Ref } from "vue";
import axiosInstance from "../../utils/axiosInstance";

const isLogged = inject<Ref<boolean>>("is-logged")!;
const userName = inject<Ref<string>>("user-name")!;
const userEmail = inject<Ref<string>>("user-email")!;
const userPicture = inject<Ref<string>>("user-picture")!;

const userBio = ref("");

const userPictureCssUrl = computed(() => {
  return `url(${userPicture.value})`;
});

function getUserInfo() {
  if (!isLogged.value) {
    return;
  }

  axiosInstance
    .get(`/profile/${userName.value}`)
    .then((response) => {
      const json = response.data as UserInfoResponse;
      userBio.value = json.bio;
    })
    .catch((error) => {
      if (error.response.status === 404) {
        console.log("Session ID not found");
      } else {
        console.log(error);
      }
    });
}
</script>

<template>
  <div class="d-flex">
    <div class="card mx-auto mt-4 w-50 position-relative bg-transparent">
      <div class="profile-card-bg position-absolute z-n1" />
      <div class="card-body">
        <img
          :src="userPicture"
          alt="profile picture"
          class="rounded-circle mx-auto d-block"
          style="width: 100px; height: 100px"
        />
        <h2 class="card-title text-center my-2 mb-4">{{ userName }}</h2>
        <p class="card-text">
          Some quick example text to build on the card title and make up the
          bulk of the card's content. asd Some quick example text to build on
          the card title and make up the bulk of the card's content. asd Some
          quick example text to build on the card title and make up the bulk of
          the card's content. asd
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-card-bg {
  height: 100%;
  width: 100%;
  background-image: v-bind(userPictureCssUrl);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;

  border-radius: 0.25rem 0.25rem 0 0;

  filter: blur(5px);
  -webkit-filter: blur(5px);
  opacity: 0.15;
}
</style>