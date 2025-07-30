<template>
  <AdminNavbar />
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="text-primary fw-bold">Manage Lots</h2>
      <button class="btn btn-success" @click="editLot(null)">
        <i class="bi bi-plus-circle me-1"></i> Create New Lot
      </button>
    </div>

    <LotSearch @search="fetchLots" />

    <div class="row justify-content-center" v-for="lot in lots" :key="lot.id">
      <div class="col-md-10 mb-4">
        <div class="card shadow rounded">
          <div
            class="card-header bg-light d-flex justify-content-between align-items-center"
          >
            <div>
              <h5 class="mb-0">Lot: {{ lot.name }} ({{ lot.location }})</h5>
              <small class="text-muted"
                >Pincode: {{ lot.pincode }} | Price: ₹{{ lot.price }}/hr</small
              >
            </div>
            <div>
              <span class="badge bg-secondary me-2"
                >Spots: {{ lot.no_of_spots }}</span
              >
              <button
                class="btn btn-sm btn-outline-primary me-2"
                @click="editLot(lot)"
              >
                Edit
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="deleteLot(lot.id)"
              >
                Delete
              </button>
            </div>
          </div>
          <div class="card-body">
            <div class="spot-grid">
              <SpotGrid
                :lotId="lot.id"
                :key="lot.id + '-' + lot.no_of_spots"
                @spot-selected="openModal"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <h4 v-if="!lots.length">
      <span class="text-center text-muted m-4"> No lots found. </span>
    </h4>

    <SpotDetailsModal
      :visible="showModal"
      :spotId="selectedSpot.id"
      :status="selectedSpot.status"
      @close="showModal = false"
    />

    <AddEditLotModal
      :visible="showAddModal"
      :lot="lotToEdit"
      @close="resetModal"
      @saved="fetchLots"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "../../services/axios";
import AdminNavbar from "../../components/admin/AdminNavbar.vue";
import SpotGrid from "../../components/admin/SpotGrid.vue";
import SpotDetailsModal from "../../components/admin/SpotDetailsModal.vue";
import AddEditLotModal from "../../components/admin/AddEditLotModal.vue";
import LotSearch from "../../components/admin/LotSearch.vue";

const lots = ref([]);
const selectedSpot = ref({});
const showModal = ref(false);

const showAddModal = ref(false);
const lotToEdit = ref(null);

const fetchLots = async (filters = {}) => {
  try {
    const { name, location, created_at_lower, no_of_spots_upper } = filters;
    const res = await axios.get("/admin/lots/filter", {
      params: {
        name,
        location,
        created_at_lower,
        no_of_spots_upper,
      },
    });
    lots.value = res.data;
  } catch (err) {
    console.error("Error fetching lots:", err);
  }
};

onMounted(fetchLots);

const openModal = (spot) => {
  selectedSpot.value = spot;
  showModal.value = true;
};

const resetModal = () => {
  showAddModal.value = false;
  lotToEdit.value = null;
};

const editLot = (lot) => {
  lotToEdit.value = { ...lot };
  showAddModal.value = true;
};

const deleteLot = async (id) => {
  if (!confirm("Are you sure you want to delete this lot?")) return;
  await axios.delete(`/admin/lots/${id}`);
  fetchLots();
};
</script>

<style scoped>
.card {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.spot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 10px;
  padding-top: 10px;
}
</style>
