<template>
  <div>
    <canvas id="priceChart"></canvas>
    <p v-if="!isDataReady">Loading chart data...</p> <!-- 데이터 로딩 중일 때 메시지 표시 -->
  </div>
</template>

<script>
import { useInvestmentStore } from '@/stores/investmentStore';
import { onMounted, computed, ref } from 'vue';
import Chart from 'chart.js/auto';

export default {
  setup() {
    const store = useInvestmentStore();
    const chart = ref(null);
    const isDataReady = computed(() => {
      return (
        store.historicalData['AAPL'] &&
        store.historicalData['AAPL'].length > 0
      );
    });

    const initializeChart = () => {
      const ctx = document.getElementById('priceChart').getContext('2d');
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: store.historicalData['AAPL'].map(d => d.date),
          datasets: Object.keys(store.historicalData).map(symbol => ({
            label: symbol,
            data: store.historicalData[symbol].map(d => d.price),
            borderColor: getRandomColor(),
            borderWidth: 1,
            tension: 0.4,
          })),
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: false,
            },
          },
        },
      });
    };

    const getRandomColor = () => {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    };

    onMounted(() => {
      if (isDataReady.value) {
        initializeChart();
      } else {
        const interval = setInterval(() => {
          if (isDataReady.value) {
            initializeChart();
            clearInterval(interval); // 데이터가 준비되면 반복 중지
          }
        }, 500); // 500ms 간격으로 데이터 준비 상태 확인
      }
    });

    return {
      isDataReady,
    };
  },
};
</script>
