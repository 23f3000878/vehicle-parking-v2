<template>
  <div class="table-responsive">
    <table class="table table-striped align-middle text-center">
      <thead class="table-light">
        <tr>
          <th>#</th>
          <th>User Email</th>
          <th>Total Revenue (₹)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(user, index) in users" :key="user.user_id">
          <td>{{ index + 1 }}</td>
          <td>{{ user.email }}</td>
          <td>₹{{ user.total_revenue.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "../../services/axios";

const users = ref([]);

onMounted(async () => {
  try {
    const res = await axios.get("/admin/users/top-revenue");
    users.value = res.data.top_users;
  } catch (err) {
    console.error("Failed to fetch top users:", err);
  }
});
</script>

<style scoped>
.table {
  border-radius: 10px;
  overflow: hidden;
}
</style>
