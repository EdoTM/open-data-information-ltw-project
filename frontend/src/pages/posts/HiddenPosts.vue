<script setup>
import PostsBasePage from "./PostsBasePage.vue";
</script>

<template>
  <PostsBasePage :show-info-alert="false" api-endpoint="/getHiddenPosts">
    <template #header>
      <i class="bi-eye-slash-fill me-3" />Hidden posts
    </template>
  </PostsBasePage>
</template>