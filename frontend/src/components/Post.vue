<script setup lang="ts">
import { bs5Breakpoints } from "../utils/appUtils";
import { computed, ref } from "vue";

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
  commentCount: number;
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

const dotsMenuOptions = ref([
  {
    text: post.hidden ? "Unhide" : "Hide",
    icon: post.hidden ? "bi-eye-slash-fill" : "bi-eye-fill",
    action: () => emit("hide", !post.hidden),
  },
  {
    text: "Report",
    icon: "bi-flag-fill text-danger",
    action: () => console.log("Report"),
  },
  {
    text: "Copy link",
    icon: "bi-link-45deg",
    action: () => console.log("Copy link"),
  },
  {
    text: "Share",
    icon: "bi-share-fill",
    action: () => console.log("Share"),
  },
]);
</script>

<template>
  <div
    class="card my-4 py-2 container d-grid"
    style="grid-template-columns: 1fr 20fr"
  >
    <div class="my-auto text-center d-flex flex-column">
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
      <div class="d-flex flex-column mx-auto">
        <a><i class="bi-chat comments-icon" /></a>
        <span v-if="commentCount > 0" class="text-center comments-text">
          {{ commentCount }}
        </span>
      </div>
    </div>
    <div class="card-body">
      <div class="d-flex">
        <h2>{{ post.title }}</h2>
        <div class="dropdown ms-auto">
          <a
            aria-expanded="false"
            class="dots-button"
            data-bs-toggle="dropdown"
          >
            <i class="bi-three-dots-vertical dots-icon"></i>
          </a>
          <ul class="dropdown-menu">
            <li v-for="(option, i) in dotsMenuOptions" :key="i">
              <a class="dropdown-item" @click="option.action">
                <i :class="option.icon" class="me-2"></i>
                {{ option.text }}
              </a>
            </li>
          </ul>
        </div>
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
  line-height: 1;
}

.star-icon {
  font-size: 1.7rem;
  color: inherit;
}

.dots-icon {
  font-size: 20px;
  color: inherit;
}

.dots-button {
  color: inherit;
  cursor: pointer;
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

.vote-button {
  color: inherit;
  cursor: pointer;
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

.comments-icon {
  font-size: 1.7rem;
  line-height: 1;
}

.comments-text {
  font-size: small;
}
</style>