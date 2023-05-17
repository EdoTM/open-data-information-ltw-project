<script lang="ts" setup>
import PlotBasePage from "./PlotBasePage.vue";
import axiosInstance from "../../utils/axiosInstance";
import { PlotElementData } from "../../types/plotElementData";

function requestPlot(index: string, elements: PlotElementData[]) {
  const requestData = { index, elements };
  return axiosInstance
    .post("/plot/tdocs", requestData)
    .then((response) => response.data as PlotDataType);
}
</script>

<template>
  <PlotBasePage
    :is-for-tdoc="true"
    :request-plot="requestPlot"
    page-title="Contributions"
  >
    Nations' or companies' <b>contributions</b> shows how much a nation or
    company has contributed to the specific category by submitting documents
    that aim to <b>change the current networking standards</b>.
  </PlotBasePage>
</template>