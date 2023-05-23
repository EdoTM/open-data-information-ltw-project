<script setup>
import PostsBasePage from "./PostsBasePage.vue";
</script>

<template>
  <PostsBasePage :show-info-alert="false" api-endpoint="/getFavoritePosts">
    <template #header> <i class="bi-star-fill me-3" />Favorite posts </template>
  </PostsBasePage>
</template>