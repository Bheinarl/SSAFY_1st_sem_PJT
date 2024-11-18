<template>
  <div>
    <h3>Current Balance: ${{ portfolio.cash.toFixed(2) }}</h3>
    <div v-for="(quantity, symbol) in portfolio.stocks" :key="symbol">
      <p><strong>{{ symbol }}</strong>: {{ quantity }} shares</p>
      <p>Value: ${{ (quantity * currentStockPrices[symbol]).toFixed(2) }}</p>
    </div>
  </div>
</template>

<script>
import { useInvestmentStore } from '@/stores/investmentStore';
import { computed } from 'vue';

export default {
  setup() {
    const store = useInvestmentStore();
    const portfolio = computed(() => store.portfolio);
    const currentStockPrices = computed(() => store.currentStockPrices);
    console.log(portfolio.stocks)

    return {
      portfolio,
      currentStockPrices
    };
  }
};

</script>


