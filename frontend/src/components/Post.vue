<script setup lang="ts">
import { bs5Breakpoints } from "../utils/appUtils";
import { computed } from "vue";

export interface PostData {
  id: number;
  title: string;
  content: string;
  postImage: string;
  authorUsername: string;
  authorProfilePic: string;
  score: number;
  userVote: UserVote;
  starred: boolean;
  timestamp: string;
  hidden: boolean;
}

const isMobile = bs5Breakpoints.smaller("md");

const post = defineProps<PostData>();
const emit = defineEmits(["upvote", "downvote", "unvote", "star", "hide"]);

const imageZoomModalId = `post-${post.id}-zoomModal`;

const displayTimestamp = computed(() => {
  const date = new Date(post.timestamp + "Z");
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  const diffDays = Math.floor(diff / (1000 * 3600 * 24));
  const diffHours = Math.floor(diff / (1000 * 3600));
  const diffMinutes = Math.floor(diff / (1000 * 60));
  const diffSeconds = Math.floor(diff / 1000);
  if (diffDays > 0) {
    return `${diffDays} days ago`;
  } else if (diffHours > 0) {
    return `${diffHours} hours ago`;
  } else if (diffMinutes > 0) {
    return `${diffMinutes} minutes ago`;
  } else {
    return `${diffSeconds} seconds ago`;
  }
});
</script>

<template>
  <div
    class="card post my-4 py-2 container d-grid"
    style="grid-template-columns: 1fr 20fr"
  >
    <div
      class="my-auto text-center d-grid"
      style="grid-template-rows: 60px auto"
    >
      <a
        class="vote-button"
        :class="userVote === 1 && 'vote-selected'"
        @click="userVote === 1 ? emit('unvote') : emit('upvote')"
      >
        <i class="bi-caret-up-fill vote-icon"></i>
      </a>
      <span class="vote-number">{{ post.score }}</span>
      <a
        class="vote-button"
        :class="userVote === -1 && 'vote-selected'"
        @click="userVote === -1 ? emit('unvote') : emit('downvote')"
      >
        <i class="bi-caret-down-fill vote-icon"></i>
      </a>
      <a
        :class="starred ? 'star-icon-selected' : 'star-button'"
        @click="starred ? emit('star', false) : emit('star', true)"
      >
        <i
          :class="starred ? 'bi-star-fill' : 'bi-star'"
          class="bi star-icon"
        ></i>
      </a>
    </div>
    <div class="card-body">
      <div class="d-flex">  
        <h2>{{ post.title }}</h2>
        <a
          class="ms-auto hide-button" 
          @click="hidden ? emit('hide', false) : emit('hide', true)"
        >
          <i 
          :class="hidden ? 'bi-eye-fill' : 'bi-eye-slash-fill'"
          class="bi hide-icon"
          ></i>
        </a>
      </div>

      <img
        alt="post-img"
        :src="post.postImage"
        :class="'post-img border ' + (!isMobile && 'float-end')"
        type="button"
        data-bs-toggle="modal"
        :data-bs-target="'#' + imageZoomModalId"
      />
      <span class="mb-2 d-flex">
        <img
          alt="username picture"
          :src="post.authorProfilePic"
          class="username-profile-picture"
        />
        <span class="my-auto username-handle">@{{ post.authorUsername }}</span>
        <span class="my-auto me-auto text-secondary"
          >&nbsp;• {{ displayTimestamp }}</span
        >
      </span>

      <p style="text-align: justify">
        {{ post.content }}
      </p>
    </div>
  </div>

  <div
    class="modal fade"
    :id="imageZoomModalId"
    tabindex="-1"
    :aria-labelledby="imageZoomModalId + 'Label'"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-body">
          <img alt="post-img" :src="post.postImage" class="w-100" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import "bootstrap/scss/bootstrap";

.post {
  width: 100%;
}

img {
  border-radius: 10px;
}

.post-img {
  margin-left: 15px;
  margin-top: 10px;
  width: 50%;
}

@include media-breakpoint-down(md) {
  .post-img {
    width: 100%;
    margin-left: 0;
    margin-bottom: 10px;
  }
}

.username-profile-picture {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  margin-right: 10px;
}

.username-handle {
  font-weight: bold;
}

.vote-icon {
  font-size: 40px;
}

.star-icon {
  font-size: 30px;
  color: inherit;
}

.hide-icon {
  font-size: 20px;
  color: inherit;
}

.hide-button {
  color: inherit;
  cursor: pointer;
}

.hide-button:hover {
  color: var(--bs-danger);
  transition-duration: 200ms;
}

.star-button {
  color: inherit;
  cursor: pointer;
}

.star-icon-selected,
.star-button:hover {
  color: var(--bs-warning);
}

.vote-number {
  font-size: 25px;
}

.vote-button:hover {
  color: var(--bs-link-color);
  transition-duration: 200ms;
  cursor: pointer;
}

.vote-selected {
  color: var(--bs-link-color) !important;
  cursor: pointer;
}

.vote-button {
  color: inherit;
  cursor: pointer;
}
</style>