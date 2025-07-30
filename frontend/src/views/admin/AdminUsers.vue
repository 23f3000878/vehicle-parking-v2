<template>
  <AdminNavbar />
  <div class="container py-4">
    <h2 class="text-center text-primary fw-bold mb-4">Registered Users</h2>

    <UserSearch @search="fetchUsers" />

    <div v-if="users.length === 0" class="alert alert-info text-center">
      No users found.
    </div>

    <div v-else class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
      <div v-for="user in users" :key="user.id" class="col">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title">{{ user.fullname }}</h5>
            <p class="card-text mb-1">
              <strong>Email:</strong> {{ user.email }}
            </p>
            <p class="card-text mb-0">
              <strong>Address:</strong> {{ user.address || "N/A" }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "../../services/axios";
import AdminNavbar from "../../components/admin/AdminNavbar.vue";
import UserSearch from "../../components/admin/UserSearch.vue";

const users = ref([]);

async function fetchUsers(filters = {}) {
  const query = new URLSearchParams(filters).toString();
  console.log(query);
  const res = await axios.get(`/admin/users?${query}`);
  users.value = res.data.users;
}

onMounted(fetchUsers);
</script>
