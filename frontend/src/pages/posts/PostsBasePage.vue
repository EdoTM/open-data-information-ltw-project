<script setup lang="ts">
import axiosInstance from "../../utils/axiosInstance";
import { onBeforeMount, ref, watch } from "vue";
import PostList from "../../components/PostList.vue";
import { PostData } from "../../types/apiTypes";

const props = defineProps<{
  apiEndpoint: string;
  showInfoAlert: boolean;
}>();

const allPosts = ref([] as PostData[]);
const shownPosts = ref([] as PostData[]);
const searchQuery = ref<string>("");
const searchByUser = ref<boolean>(false);
const loaded = ref(false);

enum SortBy {
  Newest = "Most recent",
  Oldest = "Least recent",
  MostVoted = "Most voted",
  LeastVoted = "Least voted",
}

const sortBy = ref<SortBy>(SortBy.Newest);

function getPosts() {
  axiosInstance
    .get(props.apiEndpoint)
    .then((response) => {
      allPosts.value = response.data;
      shownPosts.value = allPosts.value;
    })
    .finally(() => {
      loaded.value = true;
    });
}

function hidePost(postId: number) {
  allPosts.value = allPosts.value.filter((p) => p.id !== postId);
  shownPosts.value = shownPosts.value.filter((p) => p.id !== postId);
}

onBeforeMount(getPosts);

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
  if (newQuery.startsWith("@")) {
    shownPosts.value = allPosts.value.filter((post) =>
      post.authorUsername
        .toLowerCase()
        .includes(newQuery.slice(1).toLowerCase())
    );
    searchByUser.value = true;
    sortPosts(sortBy.value);
    return;
  } else {
    searchByUser.value = false;
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
  <div
    class="mx-auto mt-4 position-relative"
    style="max-width: 1000px; width: 90%"
  >
    <h1 class="my-4">
      <slot name="header" />
    </h1>
    <div v-if="showInfoAlert" class="alert alert-info mb-4" role="doc-abstract">
      <i class="bi-info-circle-fill me-2"></i>
      <slot name="info" />
    </div>
    <div class="d-flex flex-column flex-md-row">
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
            <a
              class="dropdown-item"
              href="#"
              @click="sortBy = SortBy.LeastVoted"
              >Least voted</a
            >
          </li>
        </ul>
      </div>
      <div class="input-group mt-2 mt-md-0 mb-md-3 ms-md-5">
        <span class="input-group-text">
          <i v-if="searchByUser" class="bi-person-fill" />
          <i v-else class="bi-search" />
        </span>
        <input
          :value="searchQuery"
          class="form-control"
          placeholder="Search the posts..."
          type="text"
          @input="handleQueryChange($event.target.value)"
        />
      </div>
    </div>
    <div
      v-if="loaded && shownPosts.length === 0 && searchQuery.length === 0"
      class="d-flex"
    >
      <h2 class="display-6 mx-auto mt-5 text-secondary">No posts to show</h2>
    </div>
    <div
      v-if="searchQuery?.length > 0 && shownPosts.length === 0"
      class="d-flex"
    >
      <h2 class="display-6 mx-auto mt-5">
        No posts matching '{{ searchQuery }}'
      </h2>
    </div>
    <PostList :posts="shownPosts" @hide-post="hidePost" />
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