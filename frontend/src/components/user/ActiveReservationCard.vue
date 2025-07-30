<template>
  <div class="card shadow-sm mb-4">
    <div class="card-body">
      <h5 class="card-title text-primary">Active Parking</h5>
      <p><strong>Location:</strong> {{ reservation.location }}</p>
      <p><strong>Vehicle:</strong> {{ reservation.vehicle_no }}</p>
      <p><strong>Parking Time:</strong> {{ formattedParkingTime }}</p>

      <button class="btn btn-danger mt-2" @click="releaseSpot">
        Release Spot
      </button>
    </div>
  </div>
</template>

<script setup>
import axios from "../../services/axios";
import { computed } from "vue";

const props = defineProps({
  reservation: Object,
  lotPrice: Number,
});

const emit = defineEmits(["refresh"]);

const formattedParkingTime = computed(() => {
  const date = new Date(props.reservation.parking_time);
  return date.toLocaleString();
});

const releaseSpot = async () => {
  const leavingTime = new Date();
  const parkingTime = new Date(props.reservation.parking_time);

  const hours = Math.max(1, (leavingTime - parkingTime) / (1000 * 60 * 60));
  const totalCost = parseFloat((hours * props.lotPrice).toFixed(2));

  const formattedTime = leavingTime
    .toISOString()
    .slice(0, 19)
    .replace("T", " ");

  try {
    await axios.put("/user/finish", {
      reservation_id: props.reservation.id,
      releasing_time: formattedTime,
      cost: totalCost,
    });

    emit("refresh");
  } catch (err) {
    console.error("Release failed:", err);
    alert("Failed to release the spot. Try again.");
  }
};
</script>
