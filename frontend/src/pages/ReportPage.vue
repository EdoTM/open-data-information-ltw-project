<script setup lang="ts">
import Post, { PostData } from "../components/Post.vue";
import md5 from "crypto-js/md5";
import {ref} from "vue";

const userVotes: any = ref([0, 1, -1]);

const posts = [
  {
    id: 0,
    title: "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    authorProfilePic: `https://www.gravatar.com/avatar/${md5("john")}?d=retro`,
    authorUsername: "@john",
    content: "Hello world!",
    image: "https://picsum.photos/500/200?random=0",
    score: -5,
  },
  {
    id: 1,
    title: "Consectetur adipiscing elit.",
    authorProfilePic: `https://www.gravatar.com/avatar/${md5("edotm")}?d=retro`,
    authorUsername: "@edotm",
    content:
      "Nel mezzo del cammin di nostra vita, mi ritrovai per una selva oscura, ché la diritta via era smarrita.",
    image: "https://picsum.photos/500/200?random=1",
    score: 10,
  },
  {
    id: 2,
    title: "Sed ut perspiciatis unde omnis iste",
    authorProfilePic: `https://www.gravatar.com/avatar/${md5(
      "franko"
    )}?d=retro`,
    authorUsername: "@franko",
    content:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." +
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    image: "https://picsum.photos/500/200?random=2",
    score: 21,
  },
];

const cons = console;
</script>

<template>
  <div class="mx-auto" style="max-width: 1000px; width: 90%">
    <h1>Report page!</h1>
    <Post
      v-for="(post, index) in posts"
      :key="post.id"
      v-bind="post"
      :userVote="userVotes[index]"
      @upvote="userVotes[index] = 1"
      @downvote="userVotes[index] = -1"
      @unvote="userVotes[index] = 0"
    />
  </div>
</template>
