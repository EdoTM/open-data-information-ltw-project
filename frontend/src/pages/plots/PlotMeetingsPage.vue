<script lang="ts" setup>
import PlotBasePage from "./PlotBasePage.vue";
import axiosInstance from "../../utils/axiosInstance";
import { PlotElementData } from "../../types/plotElementData";

function requestPlot(index: string, elements: PlotElementData[]) {
  const requestData = { index, elements };
  return axiosInstance
    .post("/plot/meetings", requestData)
    .then((response) => response.data as PlotDataType);
}
</script>

<template>
  <PlotBasePage
    :is-for-tdoc="false"
    :request-plot="requestPlot"
    page-title="Interest"
  >
    The <b>interest</b> is a measure of how much a nation or company is
    interested in the specific category. It is calculated as the total number of
    meetings of that specific category where that nation or company has
    attended.
  </PlotBasePage>
</template>