<template>
  <div>
    <h1>Stock Investment Game</h1>
    <select v-model="selectedStock" @change="fetchStockData">
      <option value="005930">Samsung Electronics</option>
      <option value="000660">SK Hynix</option>
      <option value="035420">Naver</option>
    </select>
    <canvas id="stockChart"></canvas>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  data() {
    return {
      selectedStock: "005930",
      stockData: [],
      chart: null,
    };
  },
  methods: {
    async fetchStockData() {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/stocks/${this.selectedStock}/`,
          { params: { start: "2023-01-01", end: "2023-12-31" } }
        );
        this.stockData = response.data.data;

        // 차트 업데이트
        this.updateChart();
      } catch (error) {
        console.error("Error fetching stock data:", error);
      }
    },
    updateChart() {
      const labels = this.stockData.map((item) => item.Date);
      const prices = this.stockData.map((item) => item.Close);

      if (!this.chart) {
        const ctx = document.getElementById("stockChart").getContext("2d");
        this.chart = new Chart(ctx, {
          type: "line",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Stock Price",
                data: prices,
                borderColor: "rgb(75, 192, 192)",
                tension: 0.1,
              },
            ],
          },
        });
      } else {
        this.chart.data.labels = labels;
        this.chart.data.datasets[0].data = prices;
        this.chart.update();
      }
    },
  },
  mounted() {
    this.fetchStockData(); // 초기 데이터 가져오기
  },
};
</script>
