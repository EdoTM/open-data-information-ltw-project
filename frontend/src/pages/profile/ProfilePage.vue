<script lang="ts" setup>
import { computed, inject, ref, Ref, watch } from "vue";
import axiosInstance from "../../utils/axiosInstance";

const MAX_BIO_CHARS = 100;

const isLogged = inject<Ref<boolean>>("is-logged")!;
const userName = inject<Ref<string>>("user-name")!;
const userEmail = inject<Ref<string>>("user-email")!;
const userPicture = inject<Ref<string>>("user-picture")!;

const userBio = ref("");

userBio.value = userBio.value.replace(/(^[ \t]+)/gm, "");
const editUserBio = ref(false);

const userPictureCssUrl = computed(() => {
  return `url(${userPicture.value})`;
});

function getUserInfo() {
  if (!isLogged.value) {
    console.log("suckler");
    return;
  }
  axiosInstance
    .get(`/profile/${userName.value}`)
    .then((response) => {
      const json = response.data as ProfileResponse;
      console.log(json);
      userBio.value = json.bio || "";
    })
    .catch((error) => {
      if (error.response.status === 404) {
        console.log("Session ID not found");
      } else {
        console.log(error);
      }
    });
}

function updateBio() {
  axiosInstance
    .post(`/editUser`, {
      bio: userBio.value,
    })
    .then((response) => {
      console.log(response);
    })
    .catch((error) => {
      if (error.response.status === 404) {
        console.log("Session ID not found");
      } else {
        console.log(error);
      }
    });
}

watch(isLogged, (newVal) => {
  if (newVal) {
    getUserInfo();
  }
});
</script>

<template>
  <div class="d-flex">
    <div
      class="card mx-auto mt-4 position-relative bg-transparent"
      style="max-width: 60rem"
    >
      <div class="profile-card-bg position-absolute z-n1" />
      <div class="card-body p-5">
        <img
          :src="userPicture"
          alt="profile picture"
          class="rounded-circle mx-auto d-block"
          style="width: 100px; height: 100px"
        />
        <h2 class="card-title text-center my-3 mb-4">{{ userName }}</h2>
        <div class="card mx-auto w-100 bg-transparent">
          <div class="card-body" style="width: 100vw; max-width: 100%">
            <a v-if="!editUserBio" @click="editUserBio = true"
              ><i class="bi-pencil-fill float-end px-2"
            /></a>
            <a
              v-else
              @click="
                () => {
                  editUserBio = false;
                  updateBio();
                }
              "
              ><i
                class="bi-check-lg float-end px-2"
                style="font-size: 1.6rem; line-height: 1"
            /></a>
            <h4>Bio</h4>
            <p v-if="!editUserBio && userBio.length > 0" class="card-text">
              {{ userBio }}
            </p>
            <p v-else-if="!editUserBio" class="card-text text-secondary">
              Nothing goin' on here...
            </p>
            <div v-else class="position-relative">
              <textarea
                :maxlength="MAX_BIO_CHARS"
                :value="userBio"
                class="form-control"
                style="min-height: 6rem"
                @input="userBio = $event.target.value"
              />
              <span
                v-if="userBio.length >= MAX_BIO_CHARS * 0.7"
                class="position-absolute text-danger-emphasis"
                style="right: 0.5rem; bottom: 0.5rem"
              >
                {{ userBio.length }}/{{ MAX_BIO_CHARS }}
              </span>
            </div>
          </div>
        </div>
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
  clip: rect(0, auto, auto, 0);

  border-radius: 0.25rem 0.25rem 0 0;

  filter: blur(17px);
  -webkit-filter: blur(17px);
  opacity: 0.15;
}
</style>