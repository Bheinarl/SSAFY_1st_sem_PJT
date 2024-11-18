<template>
  <div>
    <Portfolio />
    <StockChart />
    <div>
      <button @click="nextDay">Next Day</button>
    </div>
  </div>
</template>

<script>
import Portfolio from '@/components/Portfolio.vue';
import StockChart from '@/components/StockChart.vue';
import { useInvestmentStore } from '@/stores/investmentStore';

export default {
  components: { Portfolio, StockChart },
  setup() {
    const store = useInvestmentStore();
    const nextDay = store.nextDay;

    return { nextDay };
  }
};
</script>
