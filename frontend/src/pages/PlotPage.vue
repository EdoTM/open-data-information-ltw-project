<script setup lang="ts">
import { ref } from "vue";
import PlotMeetingsPage from "./plots/PlotMeetingsPage.vue";
import PlotTdocsPage from "./plots/PlotTdocsPage.vue";

const page = ref<"meetings" | "tdocs">("meetings");
</script>

<template>
  <div class="mx-auto element-grid">
    <div class="d-flex">
      <ul class="nav nav-pills mt-2 mx-auto">
        <li class="nav-item mx-1">
          <a
            class="nav-link"
            :class="page === 'meetings' && 'active'"
            aria-current="page"
            @click="page = 'meetings'"
            >Interest</a
          >
        </li>
        <li class="nav-item mx-1">
          <a
            class="nav-link"
            :class="page === 'tdocs' && 'active'"
            @click="page = 'tdocs'"
            >Contributions</a
          >
        </li>
      </ul>
    </div>

    <div v-if="page === 'meetings'">
      <PlotMeetingsPage />
    </div>
    <div v-else>
      <PlotTdocsPage />
    </div>
  </div>
</template>

<style>
.element-grid {
  max-width: 1200px;
}

.add-element-button {
  border-radius: 50%;
  width: 59px;
  height: 59px;
  font-size: 1rem;
  font-weight: bolder;
}
</style>