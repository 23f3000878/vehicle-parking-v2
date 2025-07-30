<template>
  <div class="modal d-block" tabindex="-1" v-if="visible">
    <div class="modal-dialog">
      <div class="modal-content shadow-sm">
        <div class="modal-header">
          <h5 class="modal-title">Book Parking Spot</h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
          ></button>
        </div>

        <form @submit.prevent="bookSpot">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Lot Name</label>
              <input
                type="text"
                class="form-control"
                :value="lot?.name"
                disabled
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Location</label>
              <input
                type="text"
                class="form-control"
                :value="lot?.location"
                disabled
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Spot Number</label>
              <input
                type="text"
                class="form-control"
                :value="spot?.spot_number"
                disabled
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Vehicle Number</label>
              <input
                type="text"
                class="form-control"
                v-model="vehicleNo"
                required
              />
            </div>
          </div>

          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button type="submit" class="btn btn-success">Book Now</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "../../services/axios";

const props = defineProps({
  visible: Boolean,
  lot: Object,
  spot: Object,
});
const emit = defineEmits(["close", "refresh"]);

const vehicleNo = ref("");

watch(
  () => props.visible,
  (val) => {
    if (val) vehicleNo.value = "";
  }
);

const bookSpot = async () => {
  try {
    const parking_time = new Date().toISOString();
    await axios.post("/user/book", {
      lot_id: props.lot.id,
      spot_id: props.spot.id,
      vehicle_no: vehicleNo.value,
      parking_time,
    });

    emit("refresh");
    emit("close");
  } catch (err) {
    console.error("Booking failed:", err);
    alert("Booking failed. Try again.");
  }
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.3);
}
</style>
