<script setup lang="ts">
import Post, { PostData } from "../components/Post.vue";
import axiosInstance from "../utils/axiosInstance";
import { inject, onBeforeMount, Ref, ref, watch } from "vue";

const isLogged = inject<Ref<boolean>>("is-logged")!;

const allPosts = ref([] as PostData[]);
const shownPosts = ref([] as PostData[]);
console.log(shownPosts.value);
const searchQuery = ref<string>();

enum SortBy {
  Newest = "Most recent",
  Oldest = "Least recent",
  MostVoted = "Most voted",
  LeastVoted = "Least voted",
}

const timer = ref<NodeJS.Timeout | null>(null);
const starTimer = ref<NodeJS.Timeout | null>(null);
const sortBy = ref<SortBy>(SortBy.Newest);
const showVoteAlert = ref(false);
const showStarAlert = ref(false);

function getPosts() {
  axiosInstance.get("/getPosts").then((response) => {
    allPosts.value = response.data;
    shownPosts.value = allPosts.value;
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
    });
}

onBeforeMount(getPosts);

function showVoteLoginAlert() {
  if (timer.value !== null) {
    clearTimeout(timer.value!);
  }
  showVoteAlert.value = true;
  timer.value = setTimeout(() => {
    showVoteAlert.value = false;
  }, 1000);
}

function showStarLoginAlert() {
  if (starTimer.value !== null) {
    clearTimeout(starTimer.value!);
  }
  showStarAlert.value = true;
  starTimer.value = setTimeout(() => {
    showStarAlert.value = false;
  }, 1000);
}

watch(sortBy, () => {
  sortPosts(sortBy.value);
});

function sortPosts(sort: SortBy) {
  if (sort === SortBy.Newest) {
    shownPosts.value.sort((a, b) => b.id - a.id);
  } else if (sort === SortBy.Oldest) {
    shownPosts.value.sort((a, b) => a.id - b.id);
  } else if (sort === SortBy.MostVoted) {
    shownPosts.value.sort((a, b) => b.score - a.score);
  } else if (sort === SortBy.LeastVoted) {
    shownPosts.value.sort((a, b) => a.score - b.score);
  }
}

function handleQueryChange(newQuery: string) {
  searchQuery.value = newQuery;
  if (newQuery === "") {
    shownPosts.value = allPosts.value;
    return;
  }
  shownPosts.value = allPosts.value.filter(
    (post) =>
      post.title.toLowerCase().includes(newQuery.toLowerCase()) ||
      post.content.toLowerCase().includes(newQuery.toLowerCase())
  );

  sortPosts(sortBy.value);
}
</script>

<template>
  <div class="mx-auto mt-4 position-relative" style="max-width: 1000px; width: 90%">
    <transition name="login-vote-alert">
      <div v-if="showVoteAlert" class="alert alert-danger position-fixed z-3 mt-3 ms-3" role="alert"
        style="width: max-content; left: var(--x); top: var(--y)">
        <i class="bi-exclamation-triangle-fill me-2"></i>
        You must be logged in to vote.
      </div>
    </transition>
    <transition name="login-star-alert">
      <div v-if="showStarAlert" class="alert alert-danger position-fixed z-3 mt-3 ms-3" role="alert"
        style="width: max-content; left: var(--x); top: var(--y)">
        <i class="bi-exclamation-triangle-fill me-2"></i>
        You must be logged in to star a post.
      </div>
    </transition>
    <h1 class="mb-4">User reports</h1>
    <div class="alert alert-info mb-4" role="doc-abstract">
      <i class="bi-info-circle-fill me-2"></i>
      Here users share their findings. Lorem ipsum dolor sit amet, consectetur
      adipiscing elit.
    </div>
    <div class="d-flex">
      <div class="dropdown">
        <button aria-expanded="false" class="btn btn-outline-secondary dropdown-toggle" data-bs-toggle="dropdown"
          type="button">
          <i class="bi-sort-down" /> Sort by: {{ sortBy }}
        </button>
        <ul class="dropdown-menu">
          <li>
            <a class="dropdown-item" href="#" @click="sortBy = SortBy.Newest">Most recent</a>
          </li>
          <li>
            <a class="dropdown-item" href="#" @click="sortBy = SortBy.Oldest">Least recent</a>
          </li>
          <li>
            <a class="dropdown-item" href="#" @click="sortBy = SortBy.MostVoted">Most voted</a>
          </li>
          <li>
            <a class="dropdown-item" href="#" @click="sortBy = SortBy.LeastVoted">Least voted</a>
          </li>
        </ul>
      </div>
      <div class="input-group mb-3 ms-5">
        <span class="input-group-text"><i class="bi-search" /></span>
        <input :value="searchQuery" class="form-control" placeholder="Search the posts..." type="text"
          @input="handleQueryChange($event.target.value)" />
      </div>
    </div>
    <transition-group appear name="posts">
      <div v-for="(post, i) in shownPosts" :key="post.id" :style="{ transitionDelay: `${(i + 1) * 0.1}s` }">
        <Post v-bind="post" @downvote="votePost(post, -1)" @unvote="votePost(post, 0)" @upvote="votePost(post, 1)"
          @star="starPost(post, $event)" @hide="hidePost(post, $event)" />
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