<script lang="ts" setup>
import PlotElement from "../../components/PlotElement.vue";
import plusIcon from "../../assets/plus-element.svg";
import { computed, provide, ref } from "vue";
import VChart, { THEME_KEY } from "vue-echarts";
import { SVGRenderer } from "echarts/renderers";
import { use } from "echarts/core";
import { BarChart } from "echarts/charts";
import {
  DataZoomComponent,
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
} from "echarts/components";
import { ECharts, EChartsOption } from "echarts";
import CreatePostForm from "../../components/CreatePostForm.vue";
import { PlotElementData } from "../../types/plotElementData";

const props = defineProps<{
  requestPlot: (
    index: string,
    elements: PlotElementData[]
  ) => Promise<PlotDataType>;
  pageTitle: string;
}>();

use([
  SVGRenderer,
  BarChart,
  TitleComponent,
  LegendComponent,
  GridComponent,
  TooltipComponent,
  DataZoomComponent,
]);

const categories = [
  "All",
  "Physical layer",
  "Layer 2 protocols",
  "Network protocols",
  "Security",
  "Radio performance",
  "Multimedia",
  "UE conformance",
  "Quality of service",
];

// @ts-ignore
provide(THEME_KEY, localStorage.getItem("theme"));

const plotImageData = ref<string>();

const elements = ref<(PlotElementData & { number: number })[]>([
  {
    name: "Element 1",
    color: randomColor(),
    currentCategory: categories[0],
    number: 1,
  },
]);

const elementNameNumber = computed(
  () => Math.max(...elements.value.map((e) => e.number)) + 1
);
const plotData = ref<PlotDataType>();

function randomColor() {
  return "#" + Math.floor(Math.random() * 0xffffff).toString(16);
}

function addElement() {
  elements.value.push({
    name: "Element " + elementNameNumber.value,
    color: randomColor(),
    currentCategory: categories[0],
    number: elementNameNumber.value,
  });
}

function deleteElement(index: number) {
  elements.value.splice(index, 1);
}

const chartOptions = computed(() => {
  return {
    backgroundColor: "transparent",
    tooltip: {},
    legend: {
      top: 50,
    },
    grid: {
      top: 100,
      bottom: 100,
    },
    xAxis: {
      data: plotData.value?.xAxisValues,
      axisLabel: {
        interval: 0,
        rotate: 45,
        formatter: (value) => {
          if (value.length > 15) {
            return value.substring(0, 15) + "...";
          } else {
            return value;
          }
        },
      },
    },
    yAxis: {},
    dataZoom: {
      top: {},
    },
    series: plotData.value?.elements.map((e) => ({
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

function handleRequestPlot() {
  props.requestPlot("nation", elements.value).then((data) => {
    plotData.value = data;
  });
}
</script>

<template>
  <h1>{{ pageTitle }}</h1>
  <div class="alert alert-info" role="doc-abstract">
    <i class="bi-info-circle-fill me-2"></i>
    <slot></slot>
  </div>
  <div class="d-flex flex-wrap justify-content-center">
    <transition-group name="plot-element">
      <PlotElement
        v-for="(element, i) in elements"
        :key="i"
        :categories="categories"
        :color="element.color"
        :current-category="element.currentCategory"
        :name="element.name"
        class="m-2"
        @delete="deleteElement(i)"
        @change-category="(c) => (element.currentCategory = c)"
      />
    </transition-group>
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
  <div class="my-3" style="text-align: right">
    <button
      class="btn btn-primary mx-3 my-auto align-items-center"
      type="button"
      @click="handleRequestPlot"
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
    style="width: 100%; height: 570px"
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

<style lang="scss" scoped>
.plot-element-enter-from {
  opacity: 0;
  transform: translateX(30%);
}

.plot-element-enter-active {
  transition: all 0.2s;
}

.plot-element-leave-to {
  opacity: 0;
  transform: translateY(-30%);
}

.plot-element-leave-active {
  transition: all 0.2s;
}
</style>