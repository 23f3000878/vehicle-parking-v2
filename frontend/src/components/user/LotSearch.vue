<template>
  <div class="card mb-4 p-3 shadow-sm">
    <form @submit.prevent="handleSearch" class="row g-3 align-items-end">
      <div class="col-md-10">
        <label class="form-label">Search by Location</label>
        <input
          v-model="location"
          type="text"
          class="form-control"
          placeholder="Enter location"
        />
      </div>
      <div class="col-md-2 d-flex align-items-end">
        <button type="submit" class="btn btn-primary w-100">Search</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
const emit = defineEmits(["search"]);
const location = ref("");

const handleSearch = () => {
  emit("search", { location: location.value });
};
</script>
