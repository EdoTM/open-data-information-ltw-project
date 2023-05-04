<script setup lang="ts">
defineProps<{
  elementName: string;
  elementColor: string;
  currentCategory: string;
  categories: string[];
}>();

const emit = defineEmits(["change-category"]);
</script>

<template>
  <div
    class="card plot-element d-grid pe-2"
    style="grid-template-columns: 25% auto"
  >
    <div :style="{ background: elementColor }" class="element-color m-auto" />
    <div class="element-content my-auto">
      <div class="my-2">
        <b>{{ elementName }}</b>
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
  aspect-ratio: 3;
  width: 32%;
  min-width: 300px;
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
</style>