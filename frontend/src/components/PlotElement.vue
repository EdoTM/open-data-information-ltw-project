<script setup lang="ts">
import { bs5Breakpoints } from "../utils/appUtils";
import { PlotElementData } from "../types/plotElementData";
import { ref } from "vue";

defineProps<
  PlotElementData & {
    categories: string[];
    isDeleteable: boolean;
  }
>();

const emit = defineEmits(["change-category", "delete", "change-tdoc-filter"]);

const isDesktop = bs5Breakpoints.greater("sm");

const showTdocRadios = ref(false);
</script>

<template>
  <div
    :class="[
      tdocFilter && 'py-2',
      tdocFilter && !showTdocRadios && 'plot-element-dots',
      !isDesktop && 'plot-element-sm',
    ]"
    class="card plot-element d-flex flex-column pe-2"
    id="plot-element-card"
    @mouseenter="showTdocRadios = true"
    @mouseleave="showTdocRadios = false"
  >
    <div
      :class="isDesktop && 'd-grid'"
      class="my-auto"
      style="grid-template-columns: auto 75%"
    >
      <div
        v-if="isDesktop"
        id="element-color-circle"
        :style="{ background: color }"
        class="element-color m-auto border"
      />

      <div
        id="element-info-container"
        :class="!isDesktop && 'ms-3'"
        class="element-content my-auto"
      >
        <div
          id="element-name"
          class="my-2 d-flex align-items-center"
          style="line-height: 1.2"
        >
          <span
            v-if="!isDesktop"
            :style="{ background: color }"
            class="element-color-sm"
          />
          <h5 class="m-0">{{ name }}</h5>
          <a
            :class="
              isDeleteable
                ? 'text-danger delete-element-icon'
                : 'delete-element-disabled'
            "
            class="bi bi-trash3-fill ms-auto me-2"
            @click="isDeleteable && emit('delete')"
          ></a>
        </div>
        <div id="choose-category-div" class="my-2 d-flex">
          <label class="d-inline-block" for="">Category:</label>
          <div id="category-dropdown" class="dropdown ms-1">
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
    <transition mode="out-in" name="tdoc-dots">
      <div
        v-if="tdocFilter !== undefined && showTdocRadios"
        class="d-grid"
        style="grid-template-columns: auto 75%"
      >
        <span></span>
        <div>
          <div class="form-check">
            <input
              :checked="tdocFilter === 'all'"
              :name="'radio-tdoc-coso' + name"
              class="form-check-input"
              type="radio"
              @change="emit('change-tdoc-filter', 'all')"
            />
            <label class="form-check-label"> Count all </label>
          </div>
          <div class="form-check">
            <input
              :checked="tdocFilter === 'accepted'"
              :name="'radio-tdoc-coso' + name"
              class="form-check-input"
              type="radio"
              @change="emit('change-tdoc-filter', 'accepted')"
            />
            <label class="form-check-label"> Count accepted only </label>
          </div>
          <div class="form-check">
            <input
              :checked="tdocFilter === 'rejected'"
              :name="'radio-tdoc-coso' + name"
              class="form-check-input"
              type="radio"
              @change="emit('change-tdoc-filter', 'rejected')"
            />
            <label class="form-check-label"> Count rejected only </label>
          </div>
        </div>
      </div>
      <div v-else-if="tdocFilter !== undefined" class="d-flex">
        <i class="bi-three-dots mx-auto"></i>
      </div>
    </transition>
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

.plot-element-dots {
  background: linear-gradient(
      0.5turn,
      rgba(255, 255, 255, 0) 0%,
      var(--bs-body-color) 200%
    )
    0 100px / 100% 100% no-repeat;
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

.delete-element-disabled {
  color: var(--bs-secondary-bg) !important;
  cursor: not-allowed;
}

.tdoc-dots-enter-active,
.tdoc-dots-leave-active {
  transition: all 0.1s;
}

.tdoc-dots-enter-from,
.tdoc-dots-leave-to {
  transform: translateY(18%);
}
</style>