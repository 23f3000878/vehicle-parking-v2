<template>
  <UserNavbar />
  <div class="container py-4">
    <h2 class="text-center text-primary fw-bold mb-4">Usage Summary</h2>

    <!-- Lot Selection -->
    <div class="mb-4">
      <label class="form-label fw-semibold">Select Lot</label>
      <select
        class="form-select"
        v-model="selectedLotId"
        @change="fetchLotSummary"
      >
        <option disabled value="">-- Choose a Lot --</option>
        <option v-for="lot in lots" :key="lot.id" :value="lot.id">
          {{ lot.name }} - {{ lot.location }}
        </option>
      </select>
    </div>

    <!-- Pie Chart -->
    <div v-if="lotStatusData" class="mb-5">
      <LotPieChart :data="lotStatusData" />
    </div>

    <!-- Booking History Bar Chart -->
    <div v-if="bookingHistory.length" class="mb-5">
      <BookingBarChart :chartData="bookingHistory" />
    </div>
  </div>
  <ExportButton />
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "../../services/axios";
import UserNavbar from "../../components/user/UserNavbar.vue";
import LotPieChart from "../../components/charts/LotPieChart.vue";
import BookingBarChart from "../../components/charts/BookingBarChart.vue";
import ExportButton from "../../components/user/ExportButton.vue";

const lots = ref([]);
const selectedLotId = ref("");
const lotStatusData = ref(null);
const bookingHistory = ref([]);

onMounted(async () => {
  const res = await axios.get("/user/lots");
  lots.value = res.data;
  await fetchBookingHistory(); // always load chart
});

const fetchLotSummary = async () => {
  if (!selectedLotId.value) return;
  const res = await axios.get(`/user/status-summary/${selectedLotId.value}`);
  lotStatusData.value = res.data;
};

const fetchBookingHistory = async () => {
  const res = await axios.get("/user/my-booking-history");
  bookingHistory.value = res.data;
};
</script>

<style scoped>
.container {
  max-width: 1100px;
}
</style>
