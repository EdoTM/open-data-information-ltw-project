<script setup lang="ts">
import Post, { PostData } from "../components/Post.vue";
import axiosInstance from "../utils/axiosInstance";
import { onBeforeMount, ref } from "vue";

const posts = ref([] as PostData[]);

function getPosts() {
  axiosInstance.get("/getPosts").then((response) => {
    posts.value = response.data;
  });
}

function votePost(post: PostData, vote: 1 | 0 | -1) {
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

onBeforeMount(getPosts);
</script>

<template>
  <div class="mx-auto" style="max-width: 1000px; width: 90%">
    <h1>Report page!</h1>
    <Post
      v-for="post in posts"
      :key="post.id"
      v-bind="post"
      @upvote="votePost(post, 1)"
      @downvote="votePost(post, -1)"
      @unvote="votePost(post, 0)"
    />
  </div>
</template>
