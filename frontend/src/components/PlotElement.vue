<script setup lang="ts">
import Vue3SimpleTypeahead from "vue3-simple-typeahead/src/vue3-simple-typeahead.vue";

defineProps<{
  elementName: string;
  appliedFilters: {
    filterName: string;
    filterValue: string;
  }[];
  possibleFilters: {
    filterName: string;
    filterValues: string[];
  }[];
}>();

const emit = defineEmits(["apply-filter"]);
</script>

<template>
  <div class="card" style="width: 30rem">
    <div class="card-header">Element 1</div>
    <ul class="list-group list-group-flush">
      <li v-if="appliedFilters.length === 0" class="list-group-item">
        Unfiltered.
      </li>
      <li
        v-for="(filter, i) in appliedFilters"
        :key="i"
        class="list-group-item"
      >
        {{ filter.filterName }}: {{ filter.filterValue }}
      </li>
    </ul>

    <div class="card-footer input-group">
      <button
        class="btn btn-outline-secondary dropdown-toggle"
        type="button"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        Dropdown
      </button>
      <vue3-simple-typeahead
        id="typeahead_id"
        placeholder="Start writing..."
        :items="['One', 'Two', 'Three']"
        :minInputLength="1"
      />
    </div>
  </div>
</template>

<style lang="scss">
@import "bootstrap/scss/bootstrap.scss";

.simple-typeahead-input {
  @extend .form-control;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0 10px;
  border: 0;
}

.simple-typeahead {
  @extend .form-control;
  padding: 0;
}
</style>
