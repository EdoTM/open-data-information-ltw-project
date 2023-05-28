<script setup>
import PostsBasePage from "./PostsBasePage.vue";
</script>

<template>
  <PostsBasePage :show-info-alert="true" api-endpoint="/getPosts">
    <template #header> User Reports </template>
    <template #info> Here users share their discoveries! </template>
  </PostsBasePage>
</template>