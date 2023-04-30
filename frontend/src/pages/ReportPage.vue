<script setup>
import Post from "../components/Post.vue";

const posts = [
  {
    background: "indianred",
  },
  {
    background: "yellowgreen",
  },
  {
    background: "#ccc",
  },
];
</script>

<template>
  <div>
    <h1>Report page!</h1>
    <div class="mx-auto" style="max-width: 1000px; width: 90%">
      <Post />
    </div>
  </div>
</template>
