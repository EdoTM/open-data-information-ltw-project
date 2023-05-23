<script lang="ts" setup>
import { PostData } from "../../components/Post.vue";

const post = defineProps<PostData>();
</script>

<template>
  <h1>Hello</h1>
  <Post
    :post="post"
    @downvote="downvote"
    @hide="hide"
    @star="star"
    @unvote="unvote"
    @upvote="upvote"
  />
</template>

<style scoped></style>