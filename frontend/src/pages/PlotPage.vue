<script setup lang="ts">
import { ref } from "vue";
import PlotMeetingsPage from "./plots/PlotMeetingsPage.vue";
import PlotTdocsPage from "./plots/PlotTdocsPage.vue";
import PlotElement from "../components/PlotElement.vue";

const page = ref<"meetings" | "tdocs">("meetings");

type Element = {
  name: string;
  color: string;
  currentCategory: string;
};

const elements: Element[] = [
  {
    name: "Element 1",
    color: "#f8f9fa",
    currentCategory: "Category 1",
  },
  {
    name: "Element 2",
    color: "#a56fda",
    currentCategory: "Category 2",
  },
  {
    name: "Element 3",
    color: "#dee2e6",
    currentCategory: "Category 1",
  },
  {
    name: "Element 4",
    color: "#ced4da",
    currentCategory: "Category 2",
  },
  {
    name: "Element 5",
    color: "#58aefa",
    currentCategory: "Category 1",
  },
  {
    name: "Element 6",
    color: "#e4fd45",
    currentCategory: "Category 2",
  },
  {
    name: "Element 7",
    color: "#ff61bc",
    currentCategory: "Category 1",
  },
  {
    name: "Element 8",
    color: "#e8e08c",
    currentCategory: "Category 2",
  },
  {
    name: "Element 9",
    color: "#13ffa8",
    currentCategory: "Category 1",
  },
];
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

    <div class="d-flex flex-wrap justify-content-center">
      <PlotElement
        v-for="(element, i) in elements"
        :key="i"
        :categories="['Category 1', 'Category 2']"
        :current-category="element.currentCategory"
        :element-color="element.color"
        :element-name="element.name"
        class="m-2"
        @change-category="(c) => (element.currentCategory = c)"
      />
    </div>
  </div>

  <div class="dropdown-menu rounded-3">
    <form class="p-2 mb-2 bg-body-tertiary border-bottom">
      <input
        autocomplete="false"
        class="form-control"
        placeholder="Type to filter..."
        type="search"
      />
    </form>
    <ul class="list-unstyled mb-0">
      <li>
        <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
          <span class="d-inline-block bg-success rounded-circle p-1"></span>
          Action
        </a>
      </li>
      <li>
        <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
          <span class="d-inline-block bg-primary rounded-circle p-1"></span>
          Another action
        </a>
      </li>
      <li>
        <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
          <span class="d-inline-block bg-danger rounded-circle p-1"></span>
          Something else here
        </a>
      </li>
      <li>
        <a class="dropdown-item d-flex align-items-center gap-2 py-2" href="#">
          <span class="d-inline-block bg-info rounded-circle p-1"></span>
          Separated link
        </a>
      </li>
    </ul>
  </div>
</template>

<style>
.element-grid {
  max-width: 1200px;
}
</style>