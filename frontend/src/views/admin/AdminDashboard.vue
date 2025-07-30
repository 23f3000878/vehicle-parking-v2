<template>
  <AdminNavbar />
  <div class="container py-4">
    <h2 class="mb-4 text-center fw-bold text-primary">Admin Dashboard</h2>

    <!-- Top Metrics Row -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Revenue per Lot</h5>
            <RevenueChart />
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Occupancy Trend (Last 7 Days)</h5>
            <OccupancyTrend />
          </div>
        </div>
      </div>
    </div>

    <!-- Second Row -->
    <div class="row mb-4">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Lot Availability</h5>
            <LotStatusCard />
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Top Users by Revenue</h5>
            <!-- Top Users Table -->
            <TopUsers />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import AdminNavbar from "../../components/admin/AdminNavbar.vue";
import RevenueChart from "../../components/charts/RevenueChart.vue";
import OccupancyTrend from "../../components/charts/OccupancyTrend.vue";
import LotStatusCard from "../../components/admin/LotStatusCard.vue";
import TopUsers from "../../components/admin/TopUsers.vue";
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>
