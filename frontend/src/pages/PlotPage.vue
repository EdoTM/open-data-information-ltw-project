<script setup lang="ts">
import { computed, ref } from "vue";
import PlotMeetingsPage from "./plots/PlotMeetingsPage.vue";
import PlotTdocsPage from "./plots/PlotTdocsPage.vue";
import PlotElement, { AppliedFilter } from "../components/PlotElement.vue";

const page = ref<"meetings" | "tdocs">("meetings");

const appliedFilters = ref([]);

function applyFilter({ filterName, filterValue }: AppliedFilter) {
  appliedFilters.value.push({
    filterName,
    filterValue,
  });
}

function removeFilter({ filterName }: AppliedFilter) {
  appliedFilters.value = appliedFilters.value.filter((f) => {
    return f.filterName !== filterName;
  });
}

computed(() => {
  console.log("appliedFilters changed");
  console.log(appliedFilters.value);
});
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
      @remove-filter="removeFilter"
      :applied-filters="appliedFilters"
      :element-name="'Element 1'"
    />
  </div>

  <div class="dropdown-menu rounded-3">
    <form class="p-2 mb-2 bg-body-tertiary border-bottom">
      <input type="search" class="form-control" autocomplete="false" placeholder="Type to filter...">
    </form>
    <ul class="list-unstyled mb-0">
      <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
        <span class="d-inline-block bg-success rounded-circle p-1"></span>
        Action
      </a></li>
      <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
        <span class="d-inline-block bg-primary rounded-circle p-1"></span>
        Another action
      </a></li>
      <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
        <span class="d-inline-block bg-danger rounded-circle p-1"></span>
        Something else here
      </a></li>
      <li><a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
        <span class="d-inline-block bg-info rounded-circle p-1"></span>
        Separated link
      </a></li>
    </ul>
  </div>
  
</template>
