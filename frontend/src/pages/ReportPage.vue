<script setup lang="ts">
import Post, { PostData } from "../components/Post.vue";
import axiosInstance from "../utils/axiosInstance";
import { inject, onBeforeMount, Ref, ref, watch } from "vue";

const posts = ref([] as PostData[]);

const isLogged = inject<Ref<boolean>>("is-logged")!;

function getPosts() {
  axiosInstance.get("/getPosts").then((response) => {
    posts.value = response.data;
  });
}

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

onBeforeMount(getPosts);

enum SortBy {
  Newest = "Most recent",
  Oldest = "Least recent",
  MostVoted = "Most voted",
  LeastVoted = "Least voted",
}

const timer = ref<NodeJS.Timeout | null>(null);

function showVoteLoginAlert() {
  if (timer.value !== null) {
    clearTimeout(timer.value!);
  }
  showVoteAlert.value = true;
  timer.value = setTimeout(() => {
    showVoteAlert.value = false;
  }, 4000);
}

const sortBy = ref<SortBy>(SortBy.Newest);

watch(sortBy, () => {
  const sort = sortBy.value;
  if (sort === SortBy.Newest) {
    posts.value.sort((a, b) => b.id - a.id);
  } else if (sort === SortBy.Oldest) {
    posts.value.sort((a, b) => a.id - b.id);
  } else if (sort === SortBy.MostVoted) {
    posts.value.sort((a, b) => b.score - a.score);
  } else if (sort === SortBy.LeastVoted) {
    posts.value.sort((a, b) => a.score - b.score);
  }
});

const showVoteAlert = ref(false);
</script>

<template>
  <div
    class="mx-auto mt-4 position-relative"
    style="max-width: 1000px; width: 90%"
  >
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
    <h1 class="mb-4">User reports</h1>
    <div class="alert alert-info mb-4" role="doc-abstract">
      <i class="bi-info-circle-fill me-2"></i>
      Here users share their findings. Lorem ipsum dolor sit amet, consectetur
      adipiscing elit.
    </div>
    <div class="dropdown">
      <button
        aria-expanded="false"
        class="btn btn-outline-secondary dropdown-toggle"
        data-bs-toggle="dropdown"
        type="button"
      >
        <i class="bi-sort-down" /> Sort by: {{ sortBy }}
      </button>
      <ul class="dropdown-menu">
        <li>
          <a class="dropdown-item" href="#" @click="sortBy = SortBy.Newest"
            >Most recent</a
          >
        </li>
        <li>
          <a class="dropdown-item" href="#" @click="sortBy = SortBy.Oldest"
            >Least recent</a
          >
        </li>
        <li>
          <a class="dropdown-item" href="#" @click="sortBy = SortBy.MostVoted"
            >Most voted</a
          >
        </li>
        <li>
          <a class="dropdown-item" href="#" @click="sortBy = SortBy.LeastVoted"
            >Least voted</a
          >
        </li>
      </ul>
    </div>
    <transition-group appear name="posts">
      <div
        v-for="(post, i) in posts"
        :key="post.id"
        :style="{ transitionDelay: `${(i + 1) * 0.1}s` }"
      >
        <Post
          v-bind="post"
          @downvote="votePost(post, -1)"
          @unvote="votePost(post, 0)"
          @upvote="votePost(post, 1)"
          @star="starPost(post, $event)"
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
</style>