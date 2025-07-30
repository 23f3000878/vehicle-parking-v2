<template>
  <div class="card p-3 shadow-sm mb-4">
    <form @submit.prevent="handleSearch" class="row g-3 align-items-end">
      <div class="col-md-5">
        <label class="form-label">Search by Name</label>
        <input
          v-model="name"
          class="form-control"
          placeholder="e.g. John Doe"
        />
      </div>
      <div class="col-md-5">
        <label class="form-label">Search by Address</label>
        <input
          v-model="address"
          class="form-control"
          placeholder="e.g. Delhi"
        />
      </div>
      <div class="col-md-2 d-flex justify-content-end">
        <button class="btn btn-primary w-100">Search</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
const emit = defineEmits(["search"]);

const name = ref("");
const address = ref("");

function handleSearch() {
  emit("search", {
    name: name.value || "",
    address: address.value || "",
  });
}
</script>
