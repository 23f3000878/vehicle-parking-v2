<template>
  <div>
    <h5 class="text-center mb-3 fw-bold text-primary">Booking History</h5>
    <div class="table-responsive">
      <table class="table table-striped table-hover table-bordered">
        <thead class="table-light">
          <tr>
            <th>#</th>
            <th>Vehicle No</th>
            <th>Parking Time</th>
            <th>Location</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="history.length === 0">
            <td colspan="5" class="text-center">No booking history found</td>
          </tr>
          <tr v-for="(entry, index) in history" :key="entry.id">
            <td>{{ index + 1 }}</td>
            <td>{{ entry.vehicle_no }}</td>
            <td>{{ formatDate(entry.parking_time) }}</td>
            <td>{{ entry.location }}</td>
            <td>
              <span
                :class="[
                  'badge',
                  entry.status === 'parked' ? 'bg-success' : 'bg-secondary',
                ]"
              >
                {{ entry.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from "vue";

const props = defineProps({
  history: {
    type: Array,
    default: () => [],
  },
});

const formatDate = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
};
</script>

<style scoped>
.badge {
  font-size: 0.85rem;
  padding: 0.4em 0.6em;
}
</style>
