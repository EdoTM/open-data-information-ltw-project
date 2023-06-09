<script lang="ts" setup>
import Post from "./Post.vue";
import axiosInstance from "../utils/axiosInstance";
import { inject, Ref, ref } from "vue";
import { PostData } from "../types/apiTypes";

const isLogged = inject<Ref<boolean>>("is-logged")!;

defineProps<{
  posts: PostData[];
  noCommentsModal?: boolean;
}>();

const emits = defineEmits(["hide-post"]);

const timer = ref<NodeJS.Timeout | null>(null);
const starTimer = ref<NodeJS.Timeout | null>(null);
const showVoteAlert = ref(false);
const showStarAlert = ref(false);

function votePost(post: PostData, vote: UserVote) {
  if (!isLogged.value) {
    showVoteLoginAlert();
    return;
  }
  return axiosInstance
    .post("/votePost", {
      postID: post.id,
      vote,
    })
    .then(() => {
      const diff = vote - post.userVote;
      post.score += diff;
      post.userVote = vote;
    });
}

function starPost(post: PostData, starred: boolean) {
  if (!isLogged.value) {
    showStarLoginAlert();
    return;
  }
  return axiosInstance
    .post("/starPost", {
      postID: post.id,
      starred,
    })
    .then(() => {
      post.starred = starred;
    });
}

function hidePost(post: PostData, hidden: boolean) {
  if (!isLogged.value) {
    return;
  }
  return axiosInstance
    .post("/hidePost", {
      postID: post.id,
      hidden,
    })
    .then(() => {
      post.hidden = hidden;
      emits("hide-post", post.id);
    });
}

function showVoteLoginAlert() {
  if (timer.value !== null) {
    clearTimeout(timer.value!);
  }
  showVoteAlert.value = true;
  timer.value = setTimeout(() => {
    showVoteAlert.value = false;
  }, 3500);
}

function showStarLoginAlert() {
  if (starTimer.value !== null) {
    clearTimeout(starTimer.value!);
  }
  showStarAlert.value = true;
  starTimer.value = setTimeout(() => {
    showStarAlert.value = false;
  }, 3500);
}

const actionText = {
  copyLink: "Copied link!",
  share: "Shared!",
  report: "Reported successfully.",
} as const;
type actionText = typeof actionText;

const showInfoAlert = ref(false);
const alertTimer = ref<NodeJS.Timeout | null>(null);
const alertText = ref<keyof actionText>("copyLink");

function displayInfoAlert(action: string) {
  if (alertTimer.value !== null) {
    clearTimeout(alertTimer.value!);
  }
  alertText.value = actionText[action];
  showInfoAlert.value = true;
  alertTimer.value = setTimeout(() => {
    showInfoAlert.value = false;
  }, 3500);
}
</script>

<template>
  <transition name="info-alert-copy">
    <div
      v-if="showInfoAlert"
      class="alert alert-success position-fixed z-3 start-50 translate-middle-x mt-3"
      role="alert"
      style="top: 0"
    >
      <i class="bi-check-circle-fill me-2"></i>
      {{ alertText }}
    </div>
  </transition>

  <div>
    <transition name="login-vote-alert">
      <div
        v-if="showVoteAlert"
        class="alert alert-danger position-fixed z-3 mt-3 ms-3"
        role="alert"
        style="width: max-content; left: var(--x); top: var(--y)"
      >
        <i class="bi-exclamation-triangle-fill me-2"></i>
        You must be logged in to vote.
      </div>
    </transition>
    <transition name="login-star-alert">
      <div
        v-if="showStarAlert"
        class="alert alert-danger position-fixed z-3 mt-3 ms-3"
        role="alert"
        style="width: max-content; left: var(--x); top: var(--y)"
      >
        <i class="bi-exclamation-triangle-fill me-2"></i>
        You must be logged in to star a post.
      </div>
    </transition>
    <transition-group appear name="posts">
      <div
        v-for="(post, i) in posts"
        :key="post.id"
        :style="{ transitionDelay: `${(i + 1) * 0.1}s` }"
      >
        <Post
          v-bind="post"
          @downvote="votePost(post, -1)"
          @hide="hidePost(post, $event)"
          @star="starPost(post, $event)"
          @unvote="votePost(post, 0)"
          @upvote="votePost(post, 1)"
          :no-comments-modal="noCommentsModal"
          @action="displayInfoAlert"
        />
      </div>
    </transition-group>
  </div>
</template>

<style>
.posts-enter-active,
.posts-leave-active {
  transition: all 0.3s;
}

.posts-enter-from,
.posts-leave-to {
  opacity: 0;
  transform: translateY(100%);
}

.login-vote-alert-enter-active,
.login-vote-alert-leave-active {
  transition: all 0.15s;
}

.login-vote-alert-enter-from,
.login-vote-alert-leave-to {
  opacity: 0;
  transform: scale(0);
}

.info-alert-copy-enter-active,
.info-alert-copy-leave-active {
  transition: all 0.5s;
}

.info-alert-copy-enter-from,
.info-alert-copy-leave-to {
  translate: 0 -200%;
}
</style>