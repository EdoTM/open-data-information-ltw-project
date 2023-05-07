<script setup lang="ts">
defineProps<{
  elementName: string;
  elementColor: string;
  currentCategory: string;
  categories: string[];
}>();

const emit = defineEmits(["change-category", "delete"]);
</script>

<template>
  <div
    class="card plot-element d-grid pe-2"
    style="grid-template-columns: 25% auto"
  >
    <div
      :style="{ background: elementColor }"
      class="element-color m-auto border"
    />
    <div class="element-content my-auto">
      <div class="my-2 d-flex" style="line-height: 1.2">
        <h5 class="m-0">{{ elementName }}</h5>
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
.plot-element {
  aspect-ratio: 3.5;
  width: 33%;
  min-width: 370px;
}

.element-color {
  aspect-ratio: 1;
  width: 60%;
  border-radius: 50%;
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