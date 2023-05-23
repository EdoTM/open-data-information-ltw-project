<script setup>
import PostsBasePage from "./PostsBasePage.vue";
</script>

<template>
  <PostsBasePage :show-info-alert="true" api-endpoint="/getPosts">
    <template #header> User Reports </template>
    <template #info>
      Here users share their findings. Lorem ipsum dolor sit amet, consectetur
      adipiscing elit.
    </template>
  </PostsBasePage>
</template>