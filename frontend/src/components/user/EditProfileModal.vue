<template>
  <div class="modal d-block" tabindex="-1" v-if="visible">
    <div class="modal-dialog">
      <div class="modal-content shadow">
        <div class="modal-header">
          <h5 class="modal-title">Edit Profile</h5>
          <button
            type="button"
            class="btn-close"
            @click="$emit('close')"
          ></button>
        </div>
        <form @submit.prevent="handleSubmit">
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Full Name</label>
              <input v-model="form.fullname" class="form-control" required />
            </div>
            <div class="mb-3">
              <label class="form-label">Address</label>
              <input v-model="form.address" class="form-control" />
            </div>
          </div>
          <div class="modal-footer">
            <button
              class="btn btn-secondary"
              type="button"
              @click="$emit('close')"
            >
              Cancel
            </button>
            <button class="btn btn-primary" type="submit">Update</button>
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
  userData: Object,
});
const emit = defineEmits(["close", "updated"]);

const form = reactive({
  fullname: "",
  address: "",
});

watch(
  () => props.userData,
  (val) => {
    if (val) {
      form.fullname = val.fullname || "";
      form.address = val.address || "";
    }
  },
  { immediate: true }
);

const handleSubmit = async () => {
  try {
    await axios.put("/user/profile/edit", { ...form });
    emit("updated");
    emit("close");
  } catch (err) {
    console.error("Failed to update profile", err);
    alert("Something went wrong!");
  }
};
</script>

<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.4);
}
</style>
