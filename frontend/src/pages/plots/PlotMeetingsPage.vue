<script lang="ts" setup>
import PlotElement from "../../components/PlotElement.vue";
import plusIcon from "../../assets/plus-element.svg";
import { computed, provide, ref } from "vue";
import VChart, { THEME_KEY } from "vue-echarts";
import { SVGRenderer } from "echarts/renderers";
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import {
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
} from "echarts/components";
import { ECharts, EChartsOption } from "echarts";
import CreatePostForm from "../../components/CreatePostForm.vue";

type PlotDataType = {
  xAxisValues: string[];
  elements: {
    name: string;
    data: number[];
  }[];
};

use([
  SVGRenderer,
  BarChart,
  TitleComponent,
  LegendComponent,
  GridComponent,
  TooltipComponent,
]);

// @ts-ignore
provide(THEME_KEY, localStorage.getItem("theme"));

const plotImageData = ref<string>();

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

let elementNameNumber = elements.value.length + 1;
const plotData = ref<PlotDataType>();

function randomColor() {
  return "#" + Math.floor(Math.random() * 0xffffff).toString(16);
}

function addElement() {
  elements.value.push({
    name: "Element " + elementNameNumber,
    color: randomColor(),
    currentCategory: "Category 1",
  });
  elementNameNumber++;
}

function deleteElement(index: number) {
  elements.value.splice(index, 1);
}

function getPlotData() {
  return {
    xAxisValues: ["Samsung", "Apple", "Google"],
    elements: [
      {
        name: "Element 1",
        data: [5, 10, 15],
        color: "#f8f9fa",
      },
      {
        name: "Element 2",
        data: [10, 15, 5],
        color: "#a56fda",
      },
      {
        name: "Element 3",
        data: [15, 5, 10],
        color: "#bd2f87",
      },
    ],
  };
}

function requestPlot() {
  plotData.value = getPlotData();
}

const chartOptions = computed(() => {
  return {
    backgroundColor: "transparent",
    tooltip: {},
    legend: {},
    xAxis: {
      data: plotData.value?.xAxisValues,
    },
    yAxis: {},
    series: plotData.value?.elements.map((e: any) => ({
      name: e.name,
      type: "bar",
      data: e.data,
      itemStyle: {
        color: e.color,
      },
    })),
  } as EChartsOption;
});

const plotRef = ref<ECharts>();

function shareGraph() {
  plotImageData.value = plotRef.value?.getDataURL({
    pixelRatio: 2,
    backgroundColor: "#fff",
    excludeComponents: ["toolbox"],
    type: "png",
  });
}

function publish() {
  createPostFormRef.value?.submitPost(plotImageData.value!);
}

const createPostFormRef = ref<any>();
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
  <div class="mx-auto my-3 float-end">
    <button
      class="btn btn-primary mx-3 my-auto align-items-center"
      type="button"
      @click="requestPlot"
    >
      <span class="me-2 my-auto" style="font-weight: bold; font-size: 1.3rem"
        >Plot</span
      >
      <i class="bi bi-graph-up-arrow" style="font-size: 1.5rem"></i>
    </button>
  </div>
  <div
    v-if="plotData"
    class="text-center mx-auto mb-5 mt-5"
    style="width: 800px; height: 400px"
  >
    <v-chart
      ref="plotRef"
      :option="chartOptions"
      autoscale
      class="mx-auto"
    ></v-chart>
    <button
      class="btn btn-primary mb-5"
      data-bs-target="#sharePlotModal"
      data-bs-toggle="modal"
      @click="shareGraph"
    >
      Share <i class="bi bi-share-fill"></i>
    </button>
  </div>

  <div
    id="sharePlotModal"
    aria-hidden="true"
    aria-labelledby="sharePlotModal"
    class="modal modal-xl fade"
    tabindex="-1"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h1 id="sharePlotModal" class="modal-title fs-5">Share graph</h1>
          <button
            aria-label="Close"
            class="btn-close"
            data-bs-dismiss="modal"
            type="button"
          ></button>
        </div>
        <div class="modal-body mx-5">
          <div
            class="d-flex flex-column justify-content-center align-items-center"
          >
            <img
              :src="plotImageData"
              alt="Plot"
              style="width: 100%; height: 100%; object-fit: contain"
            />
          </div>
          <CreatePostForm ref="createPostFormRef" />
        </div>
        <div class="modal-footer">
          <button
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            type="button"
          >
            Cancel
          </button>
          <button class="btn btn-primary" type="button" @click="publish">
            Publish
          </button>
        </div>
      </div>
    </div>
  </div>
</template>