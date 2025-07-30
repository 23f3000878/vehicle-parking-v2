<template>
  <div class="text-center mb-4">
    <button class="btn btn-primary" :disabled="loading" @click="startExport">
      <span v-if="loading">Exporting...</span>
      <span v-else>Export My Parking History as CSV</span>
    </button>

    <div v-if="downloadLink" class="mt-3">
      <a :href="downloadLink" download class="btn btn-success">
        Download CSV
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "../../services/axios";

const loading = ref(false);
const downloadLink = ref(null);

const startExport = async () => {
  loading.value = true;
  downloadLink.value = null;

  try {
    const res = await axios.post("/user/export-bookings");
    const taskId = res.data.task_id;

    setTimeout(() => {
      loading.value = false;
    }, 2000);
  } catch (err) {
    loading.value = false;
    alert("Failed to start export.");
  }
};
</script>
