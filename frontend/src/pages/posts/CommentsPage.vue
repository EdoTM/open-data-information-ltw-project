<script lang="ts" setup>
import PostList from "../../components/PostList.vue";
import axiosInstance from "../../utils/axiosInstance";
import Comment, { CommentData } from "../../components/Comment.vue";
import { ref } from "vue";
import { PostData } from "../../types/apiTypes";

const props = defineProps<{
  post: PostData;
  comments: CommentData[];
}>();

const emits = defineEmits(["like", "unlike", "update-comments"]);
const textarea = ref<HTMLTextAreaElement>();

function updateLike(commentId: number, liked: boolean) {
  const endpoint = liked ? "like" : "unlike";
  axiosInstance
    .get(`/${endpoint}/${commentId}`)
    .then((res) => {
      console.log(res.data);
      emits(liked ? "like" : "unlike", commentId);
    })
    .catch((err) => {
      console.log(err);
    });
}

function postComment() {
  const text = textarea.value?.value;
  if (!text) {
    return;
  }
  axiosInstance
    .post("/newComment", {
      postID: props.post.id,
      content: text,
    })
    .then((res) => {
      console.log(res.data);
      textarea.value!.value = "";
      emits("update-comments");
    })
    .catch((err) => {
      console.log(err);
    });
}
</script>

<template>
  <PostList v-if="post" :no-comments-modal="true" :posts="[post]" />
  <div class="container w-75">
    <div class="card ps-0">
      <div class="form-floating">
        <textarea
          ref="textarea"
          class="form-control"
          placeholder="Leave a comment here"
          style="height: 100px; border: transparent"
        ></textarea>
        <label>Say something scientific!</label>
        <a
          class="text-decoration-none float-end m-2 p-1 px-2 pe-3 d-flex"
          @click="postComment"
        >
          <span class="my-auto" style="line-height: 1">Send</span>
          <div class="d-inline-block my-auto" style="transform: rotate(45deg)">
            <i class="bi-send-fill" style="font-size: 1.5rem; line-height: 1" />
          </div>
        </a>
      </div>
      <ul class="list-group list-group-flush">
        <li
          v-for="comment in comments"
          :key="comment.id"
          class="list-group-item py-3 ps-0"
        >
          <Comment
            v-bind="comment"
            @like="() => updateLike(comment.id, true)"
            @unlike="() => updateLike(comment.id, false)"
          />
        </li>
      </ul>
    </div>
  </div>
</template>

<style>
.comment-author-pic {
  aspect-ratio: 1;
  border-radius: 50%;
  width: 1.5rem;
  object-fit: cover;
}

.comment-author-username {
  font-size: small;
  font-weight: bold;
}

.comment-body {
  text-align: justify;
  -webkit-hyphens: auto;
  -moz-hyphens: auto;
  hyphens: auto;
}
</style>