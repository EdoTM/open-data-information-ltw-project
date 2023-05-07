<script setup lang="ts">
import { getInputElementById } from "../utils/tsUtils";
import axiosInstance from "../utils/axiosInstance";

defineExpose({ submitPost });

function submitPost(postImage: string) {
  const form = getInputElementById("createPostForm");
  if (!form.checkValidity()) {
    form.classList.add("was-validated");
    return;
  }

  console.log("create");
  const title = getInputElementById("createPostFormTitle").value;
  const content = getInputElementById("createPostFormContent").value;
  axiosInstance
    .post("/createPost", {
      title,
      content,
      postImage,
    })
    .then(() => {
      console.log("Post created");
      window.location.href = "/report";
    })
    .catch((error) => {
      if (error.response.status === 404) {
        alert("You have to log in");
      }
      console.log(error);
    });
}
</script>

<template>
  <form id="createPostForm" class="has-validation">
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
        class="form-control"
        id="createPostFormContent"
        rows="3"
        placeholder="Write something statistical..."
      />
    </div>
  </form>
</template>