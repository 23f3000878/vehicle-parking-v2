<template>
  <div v-if="chartData">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
  <div v-else class="text-center">
    <p>Loading revenue data...</p>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "../../services/axios";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

const chartData = ref(null);
const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context) => `₹${context.parsed.y.toFixed(2)}`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      title: { display: true, text: "Revenue (₹)" },
    },
    x: {
      ticks: {
        maxRotation: 45,
        minRotation: 30,
      },
    },
  },
};

onMounted(async () => {
  try {
    const res = await axios.get("/admin/lots/revenue");
    const revenue = res.data.revenue;

    console.log(revenue);

    chartData.value = {
      labels: revenue.map((lot) => lot.name),
      datasets: [
        {
          label: "Total Revenue",
          backgroundColor: "#0d6efd",
          data: revenue.map((lot) => lot.total_revenue),
        },
      ],
    };
  } catch (err) {
    console.error("Error loading revenue data", err);
  }
});
</script>
