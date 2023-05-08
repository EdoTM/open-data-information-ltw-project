<script lang="ts" setup>
import PlotElement from "../../components/PlotElement.vue";
import plusIcon from "../../assets/plus-element.svg";
import { computed, provide, ref, watch } from "vue";
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
import axiosInstance from "../../utils/axiosInstance";
import { executeTransition } from "@vueuse/core";

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

const elements = ref<PlotElement[]>([
  {
    name: "Element 1",
    color: randomColor(),
    currentCategory: categories[0],
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
    currentCategory: categories[0],
  });
  elementNameNumber++;
}

function deleteElement(index: number) {
  elements.value.splice(index, 1);
}

function requestPlot() {
  const requestData = {
    index: "nation",
    elements: elements.value,
  };
  axiosInstance.post("/plot/meetings", requestData).then((response) => {
    plotData.value = response.data;
  });
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

const color = ref<string>();
const color1 = [12, 130, 57];
const color2 = [255, 255, 0];

const sliderValue = ref(0);

watch(sliderValue, changeSliderColor);

function changeSliderColor() {
  const value = sliderValue.value / 100;
  const r = Math.round(color1[0] * value + color2[0] * (1 - value));
  const g = Math.round(color1[1] * value + color2[1] * (1 - value));
  const b = Math.round(color1[2] * value + color2[2] * (1 - value));
  color.value = `rgb(${r}, ${g}, ${b})`;
}

function susus(event) {
  sliderValue.value = Number.parseInt(event.target.value);
}

function handleSliderChange() {
  const initialValue = sliderValue.value;
  const endValue = initialValue > 50 ? 100 : 0;
  executeTransition<number>(sliderValue, initialValue, endValue, {
    duration: 400,
    transition: [0.6, 0, 0.41, 0.98],
  });
}

const ciaone = computed(() => {
  console.log(sliderValue.value);
  return `radial-gradient(
    circle at ${sliderValue.value}% 1000%,
    ${color.value} -10%,
    transparent 100%
  )`;
});
</script>

<template>
  <h1 :style="{ color }">Meetings</h1>
  <div>
    <div class="mx-auto d-flex" style="width: 300px">
      <label class="form-label" for="customRange1">Nations</label>
      <input
        id="customRange1"
        :value="sliderValue"
        class="form-range mx-3"
        type="range"
        @change="handleSliderChange"
        @input="susus"
      />
      <label class="form-label" for="customRange1">Companies</label>
    </div>
    <div class="d-flex flex-wrap justify-content-center">
      <PlotElement
        v-for="(element, i) in elements"
        :key="i"
        :categories="categories"
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
    <div class="my-3" style="text-align: right">
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
  <div class="bg-element" />
</template>

<style scoped>
input[type="range"]::-webkit-slider-runnable-track {
  height: 25px;
  padding-top: 4px;
}

input[type="range"]::-webkit-slider-thumb {
  aspect-ratio: 1;
  width: 25px;
  height: auto;
  /*border-radius: 50%;*/
  background: v-bind(color);
  transition: 0ms;
}

.bg-element {
  background: v-bind(ciaone);
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
</style>