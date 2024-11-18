import { defineStore } from 'pinia';

export const useStockStore = defineStore('stock', {
  state: () => ({
    selectedStock: '삼성전자',
    stockMapping: {
      '삼성전자': '005930',
      'SK하이닉스': '000660',
      '현대차': '005380',
      'POSCO홀딩스': '005490',
      '두산에너빌리티': '034020',
      '셀트리온': '068270',
      'NAVER': '035420',
      '기아': '000270',
      'LG에너지솔루션': '373220',
      '롯데케미칼': '011170',
      // 다른 매핑도 추가할 수 있습니다
    }
  }),
  getters: {
    stockUrl: (state) => {
      const stockCode = state.stockMapping[state.selectedStock];
      return stockCode ? `http://127.0.0.1:8000/api/stocks/${stockCode}/` : '';
    }
  },
  actions: {
    setSelectedStock(stock) {
      this.selectedStock = stock;
    }
  }
});