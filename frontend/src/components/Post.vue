<script setup lang="ts">
import { bs5Breakpoints } from "../utils/appUtils";
import { computed, ref } from "vue";
import "../styles/Post.css";
import CommentsPage from "../pages/posts/CommentsPage.vue";
import axiosInstance from "../utils/axiosInstance";
import { CommentData, PostData } from "../types/apiTypes";
import { getDisplayTimestamp } from "../utils/postUtils";

const post = defineProps<
  PostData & {
    noCommentsModal?: boolean;
  }
>();

const postCommentCount = ref(post.commentCount);

const emit = defineEmits(["upvote", "downvote", "unvote", "star", "hide"]);

const comments = ref<CommentData[]>([]);

const isMobile = bs5Breakpoints.smaller("md");
const showCoverImage = bs5Breakpoints.smaller("md");

const imageZoomModalId = `post-${post.id}-zoomModal`;
const commentsModalId = `post-${post.id}-commentsModal`;

const displayTimestamp = computed(() => {
  return getDisplayTimestamp(post.timestamp);
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

function getComments() {
  if (post.noCommentsModal) {
    return;
  }
  axiosInstance.get(`/getComments/${post.id}`).then(
    (res) => {
      comments.value = res.data;
      postCommentCount.value = res.data.length;
      console.log("Comments", comments.value);
    },
    (err) => {
      console.log(err);
    }
  );
}

function updateLike(commentId: number, liked: boolean) {
  const comment = comments.value.find((c) => c.id === commentId);
  if (comment) {
    comment.liked = liked;
    comment.likes += liked ? 1 : -1;
  }
}
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
      <span class="vote-number my-2">{{ post.score }}</span>
      <a
        class="vote-button"
        :class="userVote === -1 && 'vote-selected'"
        @click="userVote === -1 ? emit('unvote') : emit('downvote')"
      >
        <i class="bi-caret-down-fill vote-icon"></i>
      </a>
      <a
        class="my-2"
        :class="starred ? 'star-icon-selected' : 'star-button'"
        @click="starred ? emit('star', false) : emit('star', true)"
      >
        <i
          :class="starred ? 'bi-star-fill' : 'bi-star'"
          class="bi star-icon"
        ></i>
      </a>
      <div v-if="!noCommentsModal" class="d-flex flex-column mx-auto my-2">
        <a
          :data-bs-target="'#' + commentsModalId"
          data-bs-toggle="modal"
          @click="getComments()"
          ><i class="bi-chat comments-icon"
        /></a>
        <span v-if="postCommentCount > 0" class="text-center comments-text">
          {{ postCommentCount }}
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
            <i class="bi-three-dots-vertical dots-icon ms-2"></i>
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
        :class="[
          showCoverImage ? 'post-img-cover' : 'post-img',
          'border',
          !isMobile && 'float-end',
        ]"
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
        <span class="my-auto username-handle">
          <a
            :href="`/profile?username=${post.authorUsername}`"
            class="text-decoration-none"
          >
            @{{ post.authorUsername }}
          </a>
        </span>
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

  <div
    v-if="!noCommentsModal"
    :id="commentsModalId"
    aria-hidden="true"
    class="modal fade"
    tabindex="-1"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-body">
          <CommentsPage
            :comments="comments"
            :post="post"
            @like="updateLike($event, true)"
            @unlike="updateLike($event, false)"
            @update-comments="getComments"
          />
        </div>
      </div>
    </div>
  </div>
</template>