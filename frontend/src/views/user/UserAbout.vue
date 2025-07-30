<template>
  <UserNavbar />
  <div class="container py-5">
    <h2 class="text-center mb-4 text-success fw-bold">Your Profile</h2>

    <div class="card shadow p-4 mx-auto" style="max-width: 600px">
      <ul class="list-group list-group-flush">
        <li class="list-group-item"><strong>ID:</strong> {{ user.id }}</li>
        <li class="list-group-item">
          <strong>Full Name:</strong> {{ user.fullname }}
        </li>
        <li class="list-group-item">
          <strong>Email:</strong> {{ user.email }}
        </li>
        <li class="list-group-item">
          <strong>Address:</strong> {{ user.address || "Not Provided" }}
        </li>
      </ul>
      <button class="btn btn-outline-primary me-3" @click="showModal = true">
        Edit Profile
      </button>
    </div>
  </div>
  <EditProfileModal
    :visible="showModal"
    :userData="user"
    @close="showModal = false"
    @updated="fetchUser"
  />
</template>

<script setup>
import { ref, onMounted } from "vue";
import UserNavbar from "../../components/user/UserNavbar.vue";
import axios from "../../services/axios";
import EditProfileModal from "../../components/user/EditProfileModal.vue";

const showModal = ref(false);
const user = ref({});

const fetchUser = async () => {
  try {
    const res = await axios.get("/user/me");
    user.value = res.data;
  } catch (err) {
    console.error("Failed to fetch user:", err);
  }
};

onMounted(fetchUser);
</script>

<style scoped>
.card {
  border-radius: 12px;
}
</style>
