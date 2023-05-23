<script lang="ts" setup>
import { PostData } from "../../components/Post.vue";
import PostList from "../../components/PostList.vue";
import axiosInstance from "../../utils/axiosInstance";
import Comment, { CommentData } from "../../components/Comment.vue";

defineProps<{
  post: PostData;
  comments: CommentData[];
}>();

const emits = defineEmits(["like", "unlike"]);

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
</script>

<template>
  <PostList v-if="post" :no-comments-modal="true" :posts="[post]" />
  <div class="container w-75">
    <div class="card ps-0">
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