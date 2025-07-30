<template>
  <div class="card shadow-sm mb-4">
    <div class="card-body">
      <h5 class="card-title mb-3">Reservation History</h5>
      <div class="table-responsive">
        <table class="table table-bordered align-middle">
          <thead>
            <tr class="table-light">
              <th>ID</th>
              <th>Parking Time</th>
              <th>Location</th>
              <th>Vehicle No</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-if="history.length > 0"
              v-for="reservation in history"
              :key="reservation.id"
            >
              <td>{{ reservation.id }}</td>
              <td>{{ formatDateTime(reservation.parking_time) }}</td>
              <td>{{ reservation.location }}</td>
              <td>{{ reservation.vehicle_no || "N/A" }}</td>
              <td>
                <span
                  :class="
                    reservation.status === 'released'
                      ? 'text-success fw-bold'
                      : 'text-warning fw-bold'
                  "
                >
                  {{
                    reservation.status === "released" ? "Released" : "Parked"
                  }}
                </span>
              </td>
              <td>
                <button
                  v-if="reservation.status === 'released'"
                  class="btn btn-info btn-sm"
                  @click="showInfo(reservation)"
                >
                  Info
                </button>
                <button
                  v-else
                  class="btn btn-danger btn-sm"
                  @click="releaseSpot(reservation)"
                >
                  Release
                </button>
              </td>
            </tr>
            <tr v-if="!history.length">
              <td colspan="6" class="text-center text-muted">
                No reservations found.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Info Modal -->
    <div class="modal fade show d-block" v-if="showModal" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content shadow">
          <div class="modal-header">
            <h5 class="modal-title">Reservation Information</h5>
            <button class="btn-close" @click="showModal = false"></button>
          </div>
          <div class="modal-body">
            <p><strong>ID:</strong> {{ selected.id }}</p>
            <p><strong>Location:</strong> {{ selected.location }}</p>
            <p><strong>Vehicle No:</strong> {{ selected.vehicle_no }}</p>
            <p>
              <strong>Parking Time:</strong>
              {{ formatDateTime(selected.parking_time) }}
            </p>
            <p>
              <strong>Leaving Time:</strong>
              {{ formatDateTime(selected.leaving_time) }}
            </p>
            <p><strong>Duration:</strong> {{ getDuration(selected) }}</p>
            <p><strong>Rate (per hr):</strong> ₹{{ selected.price }}</p>
            <p><strong>Total Cost:</strong> ₹{{ selected.total_cost }}</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="showModal = false">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "../../services/axios";

const props = defineProps({
  history: Array,
  lotPrice: Number,
});

const emit = defineEmits(["refresh"]);
const showModal = ref(false);
const selected = ref(null);

const showInfo = (reservation) => {
  selected.value = reservation;
  showModal.value = true;
};

const releaseSpot = async (r) => {
  try {
    const l = new Date();
    const p = new Date(parseUTC(r.parking_time));
    const hours = Math.max((l - p) / 3600000, 0.5); //atleast take for half hour
    const cost = Number((hours * r.price).toFixed(2));

    await axios.put("/user/finish", {
      reservation_id: r.id,
      releasing_time: l.toISOString(),
      cost,
    });
    emit("refresh");
  } catch (err) {
    console.error("Error releasing spot", err);
    alert("Something went wrong while releasing the spot.");
  }
};

function parseUTC(s) {
  if (!s) return null;
  // if already has timezone info, leave it; else append “Z”
  return s.match(/[zZ]|[+\-]\d{2}:\d{2}$/) ? new Date(s) : new Date(s + "Z");
}

const formatDateTime = (dt) => (dt ? parseUTC(dt).toLocaleString() : "N/A");

const getDuration = (r) => {
  if (!r.parking_time || !r.leaving_time) return "N/A";
  const p = parseUTC(r.parking_time);
  const l = parseUTC(r.leaving_time);
  const hours = ((l - p) / 3600000).toFixed(2);
  return `${hours} hours`;
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
</style>
