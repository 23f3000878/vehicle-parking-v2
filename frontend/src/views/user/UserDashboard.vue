<script setup>
import { onMounted, ref } from "vue";
import axios from "../../services/axios";
import UserNavbar from "../../components/user/UserNavbar.vue";
import ReservationTable from "../../components/user/ReservationTable.vue";
import LotCard from "../../components/user/LotCard.vue";
import LotSearch from "../../components/user/LotSearch.vue";
import BookingModal from "../../components/user/BookingModal.vue";

const bookingHistory = ref([]);
const filteredLots = ref([]);

const selectedLot = ref(null);
const selectedSpot = ref(null);
const showBookingModal = ref(false);
const lotPrice = ref(0);

onMounted(() => {
  fetchUserData();
});

const fetchUserData = async () => {
  try {
    const res1 = await axios.get("/user/reservations");
    bookingHistory.value = res1.data;

    const res2 = await axios.get("/user/lots");
    filteredLots.value = [...res2.data];
  } catch (err) {
    console.error("Error fetching data:", err);
  }
};

const handleLotSearch = async (params) => {
  const query = new URLSearchParams(params).toString();
  const res = await axios.get(`/user/lots?${query}`);
  filteredLots.value = res.data;
};

const openBookingModal = (lot, spot) => {
  selectedLot.value = lot;
  selectedSpot.value = spot;
  lotPrice.value = lot.price;
  showBookingModal.value = true;
};
</script>

<template>
  <UserNavbar />
  <div class="container py-4">
    <h2 class="text-center text-success fw-bold mb-4">User Dashboard</h2>

    <!-- Unified Reservation Table -->
    <ReservationTable
      :history="bookingHistory"
      :lotPrice="lotPrice"
      @refresh="fetchUserData"
    />

    <!-- Lot Search Bar -->
    <LotSearch @search="handleLotSearch" />

    <!-- Available Lots and SpotGrid -->
    <div class="row" v-for="lot in filteredLots" :key="lot.id">
      <div class="col-md-12 mb-4">
        <LotCard
          :lot="lot"
          :key="lot.id + '-' + lot.available_spots"
          @book="openBookingModal"
        />
      </div>
    </div>
    <h4 v-if="!filteredLots.length">
      <span class="text-center text-muted m-4"> No lots found. </span>
    </h4>
    <!-- Booking Modal -->
    <BookingModal
      :visible="showBookingModal"
      :lot="selectedLot"
      :spot="selectedSpot"
      @close="showBookingModal = false"
      @refresh="fetchUserData"
    />
  </div>
</template>

<style scoped>
.container {
  max-width: 1140px;
}
</style>
