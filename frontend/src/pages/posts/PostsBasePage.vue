<script setup lang="ts">
import { PostData } from "../../components/Post.vue";
import axiosInstance from "../../utils/axiosInstance";
import { onBeforeMount, ref, watch } from "vue";
import PostList from "../../components/PostList.vue";

const props = defineProps<{
  apiEndpoint: string;
  showInfoAlert: boolean;
}>();

const allPosts = ref([] as PostData[]);
const shownPosts = ref([] as PostData[]);
const searchQuery = ref<string>();

enum SortBy {
  Newest = "Most recent",
  Oldest = "Least recent",
  MostVoted = "Most voted",
  LeastVoted = "Least voted",
}

const sortBy = ref<SortBy>(SortBy.Newest);

function getPosts() {
  axiosInstance.get(props.apiEndpoint).then((response) => {
    allPosts.value = response.data;
    shownPosts.value = allPosts.value;
  });
}

function hidePost(post: PostData) {
  allPosts.value = allPosts.value.filter((p) => p.id !== post.id);
  shownPosts.value = shownPosts.value.filter((p) => p.id !== post.id);
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
  <div
    class="mx-auto mt-4 position-relative"
    style="max-width: 1000px; width: 90%"
  >
    <h1 class="mb-4">
      <slot name="header" />
    </h1>
    <div v-if="showInfoAlert" class="alert alert-info mb-4" role="doc-abstract">
      <i class="bi-info-circle-fill me-2"></i>
      <slot name="info" />
    </div>
    <div class="d-flex">
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
      <div class="input-group mb-3 ms-5">
        <span class="input-group-text"><i class="bi-search" /></span>
        <input
          :value="searchQuery"
          class="form-control"
          placeholder="Search the posts..."
          type="text"
          @input="handleQueryChange($event.target.value)"
        />
      </div>
    </div>
    <PostList :posts="shownPosts" @hide-post="hidePost" />
  </div>

  <div
    id="commentsPageModal"
    aria-hidden="true"
    class="modal fade"
    tabindex="-1"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5">Modal title</h1>
          <button
            aria-label="Close"
            class="btn-close"
            data-bs-dismiss="modal"
            type="button"
          ></button>
        </div>
        <div class="modal-body">...</div>
        <div class="modal-footer">
          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            type="button"
          >
            Close
          </button>
          <button class="btn btn-primary" type="button">Save changes</button>
        </div>
      </div>
    </div>
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