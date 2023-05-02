<script setup lang="ts">
import { getInputElementById } from "../utils/tsUtils";
import axiosInstance from "../utils/axiosInstance";

function onSubmit() {
  const title = getInputElementById("createPostFormTitle").value;
  const content = getInputElementById("createPostFormContent").value;
  const file = getInputElementById("createPostFormFile").files![0];
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    axiosInstance.post("/createPost", {
      title,
      content,
      postImage: reader.result,
    });
  };
}
</script>

<template>
  <form id="createPostForm" @submit="onSubmit">
    <div class="mb-3">
      <input
        required
        type="text"
        class="form-control"
        id="createPostFormTitle"
        placeholder="Post title"
      />
    </div>
    <div class="mb-3">
      <textarea
        required
        class="form-control"
        id="createPostFormContent"
        rows="3"
        placeholder="Write something statistical..."
      />
    </div>
    <div class="mb-3">
      <input
        type="file"
        required
        accept="image/*"
        class="form-control"
        id="createPostFormFile"
      />
    </div>
    <div class="mb-3">
      <button type="submit" class="btn btn-primary">Post</button>
    </div>
  </form>
</template>
