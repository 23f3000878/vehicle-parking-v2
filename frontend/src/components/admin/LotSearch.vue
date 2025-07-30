<template>
  <div class="card mb-4 p-3 shadow-sm">
    <form @submit.prevent="handleSearch" class="row gy-3 gx-3 align-items-end">
      <!-- Location -->
      <div class="col-md-3">
        <label for="location" class="form-label">Location</label>
        <input
          id="location"
          v-model="location"
          type="text"
          class="form-control"
          placeholder="e.g. Connaught Place"
        />
      </div>

      <!-- Lot Name -->
      <div class="col-md-3">
        <label for="name" class="form-label">Lot Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          class="form-control"
          placeholder="e.g. Alpha Parking"
        />
      </div>

      <!-- Created After -->
      <div class="col-md-3">
        <label for="createdAt" class="form-label">Created After</label>
        <input
          id="createdAt"
          v-model="createdAt"
          type="date"
          class="form-control"
        />
      </div>

      <!-- Max Spots -->
      <div class="col-md-3">
        <label for="maxSpots" class="form-label">Max Spots</label>
        <input
          id="maxSpots"
          v-model.number="maxSpots"
          type="number"
          min="1"
          class="form-control"
          placeholder="e.g. 100"
        />
      </div>

      <!-- Buttons -->
      <div class="col-12 d-flex justify-content-end">
        <button type="submit" class="btn btn-primary me-2">Search</button>
        <button
          type="button"
          class="btn btn-outline-secondary"
          @click="resetForm"
        >
          Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["search"]);

const location = ref("");
const name = ref("");
const createdAt = ref("");
const maxSpots = ref(null);

const handleSearch = () => {
  emit("search", {
    location: location.value || undefined,
    name: name.value || undefined,
    created_at_lower: createdAt.value || undefined,
    no_of_spots_upper: maxSpots.value || undefined,
  });
};

const resetForm = () => {
  location.value = "";
  name.value = "";
  createdAt.value = "";
  maxSpots.value = null;
  handleSearch();
};
</script>
