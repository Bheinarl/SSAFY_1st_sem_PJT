import { defineStore } from 'pinia';
import axios from 'axios';

export const useInvestmentStore = defineStore('investment', {
  state: () => ({
    currentDay: 1,
    portfolio: {
      cash: 100000,
      stocks: {}
    },
    stockData: {},
    historicalData: {},
    currentStockPrices: {},
  }),
  actions: {
    async fetchHistoricalData(symbol) {
      try {
        const API_KEY = import.meta.env.VITE_ALPHA_VANTAGE_API_KEY;
        const response = await axios.get(
          `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=${symbol}&apikey="3TM6U5JJL7MICWYF"`
        );
        console.log(`API Response for ${symbol}:`, response.data); // 응답 출력
        const timeSeriesData = response.data['Time Series (Daily)'];
        const dates = Object.keys(timeSeriesData).slice(0, 10);
        this.historicalData[symbol] = dates.map(date => ({
          date,
          price: parseFloat(timeSeriesData[date]['4. close'])
        })).reverse();
        console.log('Historical Data:', this.historicalData); // 저장된 데이터 출력
        this.currentStockPrices[symbol] = this.historicalData[symbol][0].price;
      } catch (error) {
        console.error(`Error fetching data for ${symbol}:`, error);
      }
    },
    buyStock(symbol, quantity) {
      const price = this.currentStockPrices[symbol];
      const total = price * quantity;

      if (total <= this.portfolio.cash) {
        this.portfolio.cash -= total;
        if (!this.portfolio.stocks[symbol]) {
          this.portfolio.stocks[symbol] = 0;
        }
        this.portfolio.stocks[symbol] += quantity;
      } else {
        alert('Insufficient funds!');
      }
    },
    sellStock(symbol, quantity) {
      if (this.portfolio.stocks[symbol] >= quantity) {
        const price = this.currentStockPrices[symbol];
        this.portfolio.cash += price * quantity;
        this.portfolio.stocks[symbol] -= quantity;

        if (this.portfolio.stocks[symbol] === 0) {
          delete this.portfolio.stocks[symbol];
        }
      } else {
        alert('Insufficient stocks!');
      }
    },
    nextDay() {
      if (this.currentDay < 10) {
        this.currentDay += 1;

        Object.keys(this.historicalData).forEach(symbol => {
          this.currentStockPrices[symbol] = this.historicalData[symbol][this.currentDay - 1].price;
        });
      } else {
        alert(`Game Over! Final Balance: $${this.portfolio.cash.toFixed(2)}`);
      }
    }
  }
});
