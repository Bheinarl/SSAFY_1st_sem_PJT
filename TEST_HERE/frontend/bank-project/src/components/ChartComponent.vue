<template>
  <div>
    <h2>Stock Chart</h2>
    <canvas ref="chartContainer"></canvas>
  </div>
</template>

<script setup>
import { onMounted, watch, ref } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  stockData: {
    type: Array,
    required: true
  },
  currentDay: {
    type: Number,
    required: true
  }
});

const chartContainer = ref(null);
let chartInstance = null;

const renderChart = (data, day) => {
  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = chartContainer.value.getContext('2d');
  chartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.slice(0, day).map(item => item.Date),
      datasets: [{
        label: 'Stock Price',
        data: data.slice(0, day).map(item => item.Close),
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: false
        }
      }
    }
  });
};

onMounted(() => {
  renderChart(props.stockData, props.currentDay);
});

watch([() => props.stockData, () => props.currentDay], ([newData, newDay]) => {
  renderChart(newData, newDay);
});
</script>

<style scoped>
/* 스타일 정의 */
</style>