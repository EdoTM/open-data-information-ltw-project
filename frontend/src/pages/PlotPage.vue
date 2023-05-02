<script setup lang="ts">
import { ref } from "vue";
import PlotMeetingsPage from "./plots/PlotMeetingsPage.vue";
import PlotTdocsPage from "./plots/PlotTdocsPage.vue";
import PlotElement from "../components/PlotElement.vue";

const page = ref<"meetings" | "tdocs">("meetings");

const appliedFilters = ref([]);

function applyFilter({ filterName, filterValue }) {
  appliedFilters.value.push({
    filterName,
    filterValue,
  });
}
</script>

<template>
  <div class="mx-auto" style="max-width: 800px">
    <div class="d-flex">
      <ul class="nav nav-pills mt-2 mx-auto">
        <li class="nav-item mx-1">
          <a
            class="nav-link"
            :class="page === 'meetings' && 'active'"
            aria-current="page"
            @click="page = 'meetings'"
            >Plot meetings</a
          >
        </li>
        <li class="nav-item mx-1">
          <a
            class="nav-link"
            :class="page === 'tdocs' && 'active'"
            @click="page = 'tdocs'"
            >Plot tdocs</a
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

    <PlotElement
        :key="0"
      :possible-filters="[
        {
          filterName: 'tsg',
          filterValues: ['1', '2', '3'],
        },
        {
          filterName: 'year',
          filterValues: ['2020', '2021'],
        },
      ]"
      @apply-filter="applyFilter"
      :applied-filters="[
        {
          filterName: 'tsg',
          filterValue: '1',
        },
      ]"
      :element-name="'Element 1'"
    />
  </div>
</template>