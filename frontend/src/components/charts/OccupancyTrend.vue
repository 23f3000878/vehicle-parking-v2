<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";
import axios from "../../services/axios";

const chartCanvas = ref(null);

onMounted(async () => {
  try {
    const res = await axios.get("/admin/spots/occupancy-trend");
    const trend = res.data.occupancy_trend;

    const labels = trend.map((item) => item.date);
    const data = trend.map((item) => item.occupancy_pct);

    new Chart(chartCanvas.value, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Occupancy %",
            data,
            fill: true,
            borderColor: "#36A2EB",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: { display: true, text: "%" },
            ticks: {
              callback: (val) => val + "%",
            },
          },
        },
      },
    });
  } catch (err) {
    console.error("Failed to fetch occupancy trend:", err);
  }
});
</script>

<style scoped>
div {
  min-height: 300px;
}
</style>
