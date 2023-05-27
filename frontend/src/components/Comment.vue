<script lang="ts" setup>
import { getDisplayTimestamp } from "../utils/postUtils";
import { computed } from "vue";
import { CommentData } from "../types/apiTypes";
import { escapeHtml } from "@vue/shared";

const props = defineProps<CommentData>();
const emits = defineEmits(["like", "unlike"]);

const displayTimestamp = computed(() => {
  return getDisplayTimestamp(props.timestamp);
});

const formattedContent = computed(() => {
  if (!props.content) {
    return "";
  }
  // replace @username with link to profile
  const sanitizedContent = escapeHtml(props.content);
  console.log(sanitizedContent);
  return sanitizedContent.replace(
    /@([a-zA-Z0-9_-]+)/g,
    `<a class="text-decoration-none p-0 m-0" href="/profile?username=$1">
      <span class="username-handle-comment">@$1</span></a>`
  );
});
</script>

<template>
  <div class="d-grid" style="grid-template-columns: 3rem auto">
    <div class="d-flex flex-column m-auto">
      <a
        ><i
          :class="liked ? 'bi-caret-up-fill like-icon-active' : 'bi-caret-up'"
          class="like-icon"
          @click="liked ? emits('unlike') : emits('like')"
      /></a>
      <span v-if="likes > 0" class="text-center likes-text">{{ likes }}</span>
    </div>
    <div>
      <span class="me-3">
        <img
          :src="authorProfilePic"
          alt="comment author profile pic"
          class="comment-author-pic"
        />
        <span class="comment-author-username">
          <a
            :href="`/profile?username=${authorUsername}`"
            class="text-decoration-none"
          >
            @{{ authorUsername }}
          </a>
        </span>
      </span>
      <span class="comment-body" v-html="formattedContent"> </span>
      <span class="text-secondary small">&nbsp; – {{ displayTimestamp }}</span>
    </div>
  </div>
</template>

<style scoped>
.like-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.like-icon:hover,
.like-icon-active {
  color: orange;
}

.likes-text {
  font-size: 0.8rem;
}
</style>

<style>
.username-handle-comment {
  font-weight: 500;
}
</style>