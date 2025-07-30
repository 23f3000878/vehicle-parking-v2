<template>
  <div>
    <canvas ref="barChart"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "../../services/axios";

const barChart = ref(null);

onMounted(async () => {
  try {
    const res = await axios.get("/admin/lots/availability");
    const lots = res.data.availability;

    const labels = lots.map((lot) => lot.name);
    const available = lots.map((lot) => lot.available_spots);
    const occupied = lots.map((lot) => lot.occupied_spots);

    new Chart(barChart.value, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Available Spots",
            data: available,
            backgroundColor: "#28a745", // Green
          },
          {
            label: "Occupied Spots",
            data: occupied,
            backgroundColor: "#dc3545", // Red
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "top" },
          title: {
            display: false,
          },
        },
        scales: {
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 30,
            },
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Spots",
            },
          },
        },
      },
    });
  } catch (err) {
    console.error("Failed to fetch lot availability", err);
  }
});
</script>

<style scoped>
div {
  min-height: 300px;
}
</style>
