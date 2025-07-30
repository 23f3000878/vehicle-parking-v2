<template>
  <div class="card shadow-sm rounded h-100">
    <div class="card-body">
      <h5 class="mb-3 text-center fw-semibold">
        Lot Status (Available vs Occupied)
      </h5>
      <canvas ref="chartCanvas" style="max-height: 280px"></canvas>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";

Chart.register(PieController, ArcElement, Tooltip, Legend);

const props = defineProps(["data"]);
const chartCanvas = ref(null);
let chartInstance = null;

const createChart = () => {
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(chartCanvas.value, {
    type: "pie",
    data: {
      labels: ["Available", "Occupied"],
      datasets: [
        {
          data: [props.data.available, props.data.occupied],
          backgroundColor: ["#28a745", "#dc3545"],
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
};

onMounted(createChart);
watch(() => props.data, createChart);
</script>
