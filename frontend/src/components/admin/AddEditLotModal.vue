<template>
  <div class="modal d-block" tabindex="-1" v-if="visible">
    <div class="modal-dialog modal-lg">
      <div class="modal-content shadow-sm">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ lot && lot.id ? "Edit Lot" : "Add New Lot" }}
          </h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
          ></button>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div class="row g-3">
              <div class="col-md-6">
                <label class="form-label">Lot Name</label>
                <input v-model="form.name" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Prime Location</label>
                <input
                  v-model="form.prime_location_name"
                  class="form-control"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Address</label>
                <input v-model="form.address" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Pincode</label>
                <input v-model="form.pincode" class="form-control" required />
              </div>

              <div class="col-md-6">
                <label class="form-label">Price per Hour (₹)</label>
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  v-model="form.price"
                  class="form-control"
                  required
                />
              </div>

              <div class="col-md-6">
                <label class="form-label">Total Spots</label>
                <input
                  type="number"
                  min="1"
                  v-model="form.no_of_spots"
                  class="form-control"
                  required
                />
              </div>
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
            <button type="submit" class="btn btn-primary">
              {{ lot && lot.id ? "Update" : "Add" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue";
import axios from "../../services/axios";

const props = defineProps({
  visible: Boolean,
  lot: Object,
});

const emit = defineEmits(["close", "saved"]);

const form = reactive({
  name: "",
  prime_location_name: "",
  address: "",
  pincode: "",
  price: "",
  no_of_spots: "",
});

watch(
  () => props.lot,
  (lot) => {
    if (lot) {
      form.name = lot.name || "";
      form.prime_location_name = lot.location || "";
      form.address = lot.address || "";
      form.pincode = lot.pincode || "";
      form.price = lot.price || "";
      form.no_of_spots = lot.no_of_spots || "";
    } else {
      Object.keys(form).forEach((key) => (form[key] = ""));
    }
  },
  { immediate: true }
);

const handleSubmit = async () => {
  try {
    if (props.lot && props.lot.id) {
      await axios.put(`/admin/lots/${props.lot.id}`, { ...form });
    } else {
      await axios.post("/admin/lots", { ...form });
    }

    emit("saved");
    emit("close");
  } catch (err) {
    console.error("Error saving lot:", err);
    alert("Something went wrong. Please try again.");
  }
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.3);
}
</style>
