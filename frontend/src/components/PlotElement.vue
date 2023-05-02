<script setup>
const appliedFilters = [
  "filter1",
  "filter2",
  "filter3",
]
</script>

<template>
  <div class="card" style="width: 18rem;">
    <div class="card-header">
      Element 1
    </div>
    <ul class="list-group list-group-flush">
      <li v-for="(filter, i) in appliedFilters" :key="i" class="list-group-item">{{ filter }}</li>
    </ul>
  </div>

  <div class="dropdown">
    <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">
      Dropdown button
    </button>
    <ul class="dropdown-menu">
      <li><input class="dropdown-item form-control" id="myInput" type="text" placeholder="Search.." @keyup=""></li>
      <li><a class="dropdown-item" href="#">Action</a></li>
      <li><a class="dropdown-item" href="#">Another action</a></li>
      <li><a class="dropdown-item" href="#">Something else here</a></li>
    </ul>
  </div>
</template>
