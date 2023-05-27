<script lang="ts" setup>
import { computed, inject, onMounted, ref, Ref } from "vue";
import axiosInstance from "../../utils/axiosInstance";
import { ProfileInfo } from "../../types/apiTypes";
import PostList from "../../components/PostList.vue";
import { useRoute, useRouter } from "vue-router";

const MAX_BIO_CHARS = 100;

const localUserName = inject<Ref<string>>("user-name")!;

const username = ref("");

const router = useRouter();

const userInfo = ref<ProfileInfo>({
  bio: "",
  email: "",
  birthday: "",
  posts: [],
  postCount: 0,
  profile_pic: "",
  username: "",
});

const postsText = computed(() => {
  return userInfo.value.postCount === 1 ? "post" : "posts";
});

const editUserBio = ref(false);

const userPictureCssUrl = computed(() => {
  return `url(${userInfo.value.profile_pic})`;
});

function getUserInfo(username: string) {
  axiosInstance
    .get(`/profile/${username}`)
    .then((response) => {
      const json = response.data as ProfileInfo;
      console.log(json);
      userInfo.value = json;
      userInfo.value.username = "@" + json.username;
      userInfo.value.bio = json.bio.replace(/(^[ \t]+)/gm, "");
    })
    .catch((error) => {
      if (error.response.status === 404) {
        router.push("/profile404");
      } else {
        console.log(error);
      }
    });
}

function updateBio() {
  axiosInstance
    .post(`/editUser`, {
      bio: userInfo.value.bio,
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

onMounted(() => {
  const { username } = useRoute().query as string;
  if (username) {
    getUserInfo(username);
  } else {
    router.push("/");
  }
});
</script>

<template>
  <div class="d-flex flex-column">
    <div class="mx-auto">
      <div
        class="card mt-4 position-relative bg-transparent"
        style="max-width: 60rem; width: 100vw"
      >
        <div class="profile-card-bg position-absolute z-n1" />
        <div class="card-body p-5">
          <img
            :src="userInfo.profile_pic"
            alt="profile picture"
            class="rounded-circle mx-auto d-block"
            style="width: 100px; height: 100px"
          />
          <h2 class="card-title text-center my-3">{{ userInfo.username }}</h2>
          <h4 class="card-title text-center my-3 mb-5">
            {{ userInfo.postCount }} {{ postsText }}
          </h4>
          <div class="card mx-auto w-100 bg-transparent">
            <div class="card-body">
              <a
                v-if="!editUserBio && localUserName === userInfo.username"
                @click="editUserBio = true"
                ><i class="bi-pencil-fill float-end px-2"
              /></a>
              <a
                v-else-if="localUserName === userInfo.username"
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
              <p
                v-if="!editUserBio && userInfo.bio.length > 0"
                class="card-text"
                style="white-space: pre-line"
              >
                {{ userInfo.bio }}
              </p>
              <p v-else-if="!editUserBio" class="card-text text-secondary">
                Nothing goin' on here...
              </p>
              <div v-else class="position-relative">
                <textarea
                  :maxlength="MAX_BIO_CHARS"
                  :value="userInfo.bio"
                  class="form-control"
                  style="min-height: 6rem"
                  @input="userInfo.bio = $event.target.value"
                />
                <span
                  v-if="userInfo.bio.length >= MAX_BIO_CHARS * 0.7"
                  class="position-absolute text-danger-emphasis"
                  style="right: 0.5rem; bottom: 0.5rem"
                >
                  {{ userInfo.bio.length }}/{{ MAX_BIO_CHARS }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="mx-auto" style="max-width: 1000px">
        <h2 class="text-center my-5">User posts</h2>
        <PostList :posts="userInfo.posts" />
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