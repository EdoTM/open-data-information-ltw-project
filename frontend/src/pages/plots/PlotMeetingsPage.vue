<script lang="ts" setup>
import PlotElement from "../../components/PlotElement.vue";
import plusIcon from "../../assets/plus-element.svg";
import { ref } from "vue";

const elements = ref<PlotElement[]>([
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
]);

function randomColor() {
  return "#" + Math.floor(Math.random() * 0xffffff).toString(16);
}

function addElement() {
  elements.value.push({
    name: "Element " + (elements.value.length + 1),
    color: randomColor(),
    currentCategory: "Category 1",
  });
}

function deleteElement(index: number) {
  elements.value.splice(index, 1);
}
</script>

<template>
  <h1>Meetings</h1>
  <div class="d-flex flex-wrap justify-content-center">
    <PlotElement
      v-for="(element, i) in elements"
      :key="i"
      :categories="['Category 1', 'Category 2']"
      :current-category="element.currentCategory"
      :element-color="element.color"
      :element-name="element.name"
      class="m-2"
      @delete="deleteElement(i)"
      @change-category="(c) => (element.currentCategory = c)"
    />
    <button
      class="btn btn-success mx-3 add-element-button my-auto"
      type="button"
      @click="addElement"
    >
      <img
        :src="plusIcon"
        alt="Add"
        style="width: 1.7rem; filter: invert(100%)"
      />
    </button>
  </div>
</template>