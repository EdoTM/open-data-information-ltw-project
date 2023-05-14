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

function votePost(post: PostData, vote: UserVote) {
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
    <transition-group appear name="posts">
      <div
        v-for="post in posts"
        :key="post.id"
        :style="{
          transitionDelay: `${(posts.indexOf(post) + 1) * 0.1}s`,
        }"
      >
        <Post
          v-bind="post"
          @downvote="votePost(post, -1)"
          @unvote="votePost(post, 0)"
          @upvote="votePost(post, 1)"
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
</style>