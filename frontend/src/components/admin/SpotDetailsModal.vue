<template>
  <div class="modal fade show d-block" tabindex="-1" v-if="visible">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content shadow">
        <div class="modal-header">
          <h5 class="modal-title">
            Spot Details - #{{ spot?.spot_number || spotId }}
          </h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>

        <div class="modal-body">
          <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary"></div>
          </div>

          <div v-else-if="error" class="alert alert-danger">
            Spot details not found or an error occurred.
          </div>

          <div v-else>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">
                <strong>Status:</strong>
                <span
                  :class="{
                    'text-success': spot.status === 'A',
                    'text-danger': spot.status === 'O',
                  }"
                >
                  {{ spot.status === "A" ? "Available" : "Occupied" }}
                </span>
              </li>

              <li class="list-group-item" v-if="spot.vehicle_no">
                <strong>Vehicle No:</strong> {{ spot.vehicle_no }}
              </li>
              <li class="list-group-item" v-if="spot.reserved_by">
                <strong>Reserved By:</strong> {{ spot.reserved_by }}
              </li>
              <li class="list-group-item" v-if="spot.parking_time">
                <strong>Parking Time:</strong>
                {{ formatDateTime(spot.parking_time) }}
              </li>
              <li class="list-group-item" v-if="spot.estimated_cost">
                <strong>Estimated Cost:</strong> ₹{{
                  estimatedCost(spot.estimated_cost, spot.parking_time)
                }}
              </li>
            </ul>
          </div>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "../../services/axios";

const props = defineProps({
  visible: Boolean,
  spotId: Number,
  status: String,
});

const emit = defineEmits(["close"]);

const spot = ref(null);
const loading = ref(false);
const error = ref(false);

watch(
  () => props.visible,
  async (val) => {
    if (val && props.spotId) {
      loading.value = true;
      error.value = false;
      spot.value = null;

      try {
        const endpoint =
          props.status === "O"
            ? `/admin/spots/${props.spotId}/occupied`
            : `/admin/spots/${props.spotId}`;
        const res = await axios.get(endpoint);
        spot.value = res.data.spot;
      } catch (err) {
        error.value = true;
        console.error(err);
      } finally {
        loading.value = false;
      }
    }
  }
);

const formatDateTime = (dt) => {
  if (!dt) return "-";
  return new Date(dt).toLocaleString();
};

const estimatedCost = (price, parking_time) => {
  const parkingDate = new Date(parking_time);
  const now = new Date();

  const diffInHours = Math.max((now - parkingDate) / (1000 * 60 * 60), 0.5);

  // Prevent negative charges
  if (diffInHours <= 0) return 0;

  return +(diffInHours * price).toFixed(2);
};

const closeModal = () => {
  emit("close");
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
