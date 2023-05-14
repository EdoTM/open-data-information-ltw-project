<script setup lang="ts">
import { bs5Breakpoints } from "../utils/appUtils";
import { PlotElementData } from "../types/plotElementData";

defineProps<
  PlotElementData & {
    categories: string[];
  }
>();

const emit = defineEmits(["change-category", "delete"]);

const isDesktop = bs5Breakpoints.greater("sm");
</script>

<template>
  <div
    :class="!isDesktop && ['d-flex plot-element-sm']"
    class="card plot-element pe-2 d-grid"
    style="grid-template-columns: auto 75%"
    id="plot-element-card"
  >
    <div
      v-if="isDesktop"
      :style="{ background: color }"
      class="element-color m-auto border"
    />
    <div :class="!isDesktop && 'ms-3'" class="element-content my-auto">
      <div class="my-2 d-flex align-items-center" style="line-height: 1.2">
        <span
          v-if="!isDesktop"
          :style="{ background: color }"
          class="element-color-sm"
        />
        <h5 class="m-0">{{ name }}</h5>
        <a
          class="bi bi-trash3-fill ms-auto me-2 text-danger delete-element-icon"
          @click="emit('delete')"
        ></a>
      </div>
      <div class="my-2 d-flex">
        <label class="d-inline-block" for="">Category:</label>
        <div class="dropdown ms-1">
          <button
            aria-expanded="false"
            class="btn btn-outline-secondary dropdown-toggle ms-1"
            data-bs-toggle="dropdown"
            type="button"
          >
            {{ currentCategory }}
          </button>
          <ul class="dropdown-menu">
            <li v-for="(category, i) in categories" :key="i">
              <a
                class="dropdown-item"
                href="#"
                @click="emit('change-category', category)"
                >{{ category }}</a
              >
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --x: 0.5;
  --y: 0.5;
}

.plot-element {
  aspect-ratio: 3.5;
  width: 33%;
  min-width: 370px;
}

.plot-element-sm {
  aspect-ratio: 3;
  min-width: 300px;
}

.element-color {
  aspect-ratio: 1;
  width: 60%;
  border-radius: 50%;
}

.element-color-sm {
  aspect-ratio: 1;
  width: 7%;
  border-radius: 50%;
  margin-right: 0.5rem;
}

.element-content {
  font-size: 1.2rem;
  line-height: 1.8;
}

.delete-element-icon:not(:hover) {
  color: inherit !important;
}

.delete-element-icon {
  transition-duration: 100ms;
}
</style>