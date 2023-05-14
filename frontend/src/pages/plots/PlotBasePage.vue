<script lang="ts" setup>
import PlotElement from "../../components/PlotElement.vue";
import plusIcon from "../../assets/plus-element.svg";
import { computed, inject, nextTick, provide, Ref, ref, watch } from "vue";
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
import { Tooltip } from "bootstrap";

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

const isLogged = inject<Ref<boolean>>("is-logged")!;

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
  const category =
    categories.filter(
      (c) => !elements.value.map((e) => e.currentCategory).includes(c)
    )[0] ?? categories[0];

  elements.value.push({
    name: "Element " + elementNameNumber.value,
    color: randomColor(),
    currentCategory: category,
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
const tooltip = ref<Tooltip>();

function createTooltip() {
  const tooltipTrigger = document.getElementById("shareButtonTooltip");
  tooltip.value = new Tooltip(tooltipTrigger);
}

function handleRequestPlot() {
  props.requestPlot(plotIndex.value, elements.value).then((data) => {
    plotData.value = data;
    if (!isLogged.value) {
      console.log("here");
      nextTick(createTooltip);
    }
  });
}

watch(isLogged, () => {
  console.log("isLogged changed");
  if (isLogged.value) {
    // @ts-ignore
    tooltip.value?.disable();
  } else if (plotData.value) {
    console.log("enabling...");
    // @ts-ignore
    tooltip.value?.enable();
    console.log(tooltip.value);
  }
});

const sliderValue = ref<0 | 1>(0);
const plotIndex = computed(() =>
  sliderValue.value === 0 ? "nation" : "company"
);
</script>

<template>
  <div class="px-3">
    <h1>{{ pageTitle }}</h1>
    <div class="alert alert-info" role="doc-abstract">
      <i class="bi-info-circle-fill me-2"></i>
      <slot></slot>
    </div>
    <div class="mx-auto" style="width: 230px">
      <div class="d-grid" style="grid-template-columns: 30% 40% 30%">
        <span class="ms-auto">Nations</span>
        <input
          id="indexChooserSlider"
          :value="sliderValue"
          class="form-range mx-auto"
          max="1"
          min="0"
          style="width: 50px"
          type="range"
          @change="sliderValue = ($event.target.value * 1) as 0 | 1"
        />
        <span class="me-auto">Companies</span>
      </div>
    </div>
    <div class="d-flex flex-wrap justify-content-center">
      <transition-group name="plot-element">
        <PlotElement
          v-for="(element, i) in elements"
          :key="i"
          :categories="categories"
          :color="element.color"
          :current-category="element.currentCategory"
          :is-deleteable="elements.length > 1"
          :name="element.name"
          class="m-2"
          @delete="deleteElement(i)"
          @change-category="(c) => (element.currentCategory = c)"
        />
      </transition-group>
      <button
        v-if="elements.length < categories.length"
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
      <span
        id="shareButtonTooltip"
        class="d-inline-block"
        data-bs-title="You must be logged in to share the graph."
        tabindex="0"
      >
        <button
          :data-bs-toggle="isLogged && 'modal'"
          :disabled="!isLogged"
          class="btn btn-primary mb-5"
          data-bs-target="#sharePlotModal"
          @click="shareGraph"
        >
          Share <i class="bi bi-share-fill"></i>
        </button>
      </span>
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

.plot-element-leave-active {
  transition: all 0.15s;
}

.plot-element-leave-to {
  opacity: 0;
  transform: scale(0.5);
}
</style>