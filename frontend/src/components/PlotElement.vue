<script setup lang="ts">
import Vue3SimpleTypeahead from "vue3-simple-typeahead/src/vue3-simple-typeahead.vue";
import { computed, ref } from "vue";

export type Filter = {
  filterName: string;
  filterValues: string[];
};

export type AppliedFilter = {
  filterName: string;
  filterValue: string;
};

const props = defineProps<{
  elementName: string;
  appliedFilters: AppliedFilter[];
  possibleFilters: Filter[];
}>();

const emit = defineEmits(["apply-filter", "remove-filter"]);

const availableFilters = computed<Filter[]>(() => {
  return props.possibleFilters.filter((f) => {
    return !props.appliedFilters.some(
      (appliedFilter) => appliedFilter.filterName === f.filterName
    );
  });
});

const selectedFilter = ref<Filter>();
const currentInputText = ref("");

function handleSelectFilter(event: any) {
  const value: string = event.target.value;
  if (value === "") {
    return;
  }
  selectedFilter.value = availableFilters.value.find(
    (f) => f.filterName === value
  );
}

function handleRemoveFilter(event: any) {
  const value: string = event.target.value;
  if (value === "") {
    return;
  }
  selectedFilter.value = availableFilters.value.find(
      (f) => f.filterName === value
  );
}

function handleSelectFilterValue(value: string) {
  console.log(value);
  emit("apply-filter", {
    filterName: selectedFilter.value!.filterName,
    filterValue: value,
  });
  selectedFilter.value = undefined;
}
</script>

<template>
  <div class="card" style="width: 30rem">
    <div class="card-header">Element 1</div>
    <ul class="list-group list-group-flush">
      <li v-if="appliedFilters.length === 0" class="list-group-item">
        Unfiltered.
      </li>
      <li
        v-for="(appliedFilter, i) in appliedFilters"
        :key="i"
        class="list-group-item"
      >
        <button
          class="btn btn-outline-danger p-1 me-2"
          style="width: 35px; height: 35px"
          @click="emit('remove-filter', appliedFilter)"
        >
          <i class="bi-trash3-fill" />
        </button>
        <span
          >{{ appliedFilter.filterName }}: {{ appliedFilter.filterValue }}</span
        >
      </li>
    </ul>

    <div class="card-footer input-group" v-if="availableFilters.length > 0">
      <select
        @change="handleSelectFilter"
        class="form-select"
        aria-label="Default select example"
        :value="selectedFilter?.filterName || ''"
      >
        <option selected value="">Select filter...</option>
        <option v-for="(filter, i) in availableFilters" :key="i">
          {{ filter.filterName }}
        </option>
      </select>
      <vue3-simple-typeahead
          select-on-tab
        id="typeahead_id"
        placeholder="Start writing..."
        :items="selectedFilter?.filterValues || []"
        :minInputLength="0"
        :disabled="selectedFilter === undefined"
        @select-item="handleSelectFilterValue"
        @on-input="currentInputText = $event.input"
          :value="selectedFilter === undefined ? '' : currentInputText"
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
