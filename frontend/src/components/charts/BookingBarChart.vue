<template>
  <div class="card shadow-sm rounded h-100">
    <div class="card-body">
      <h5 class="card-title text-center mb-3 fw-semibold">
        Booking History (Last 7 Days)
      </h5>
      <canvas ref="chartRef" style="max-height: 280px"></canvas>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import Chart from "chart.js/auto";

const props = defineProps(["chartData"]);
const chartRef = ref(null);
let chartInstance = null;

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  const labels = props.chartData.map((item) => item.date.slice(5));
  const counts = props.chartData.map((item) => item.count);

  chartInstance = new Chart(chartRef.value, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Bookings",
          data: counts,
          backgroundColor: "#198754",
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
    },
  });
};

onMounted(renderChart);
watch(() => props.chartData, renderChart);
</script>
