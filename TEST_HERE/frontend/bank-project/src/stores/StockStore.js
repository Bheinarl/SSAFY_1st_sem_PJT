import { defineStore } from 'pinia';

export const useStockStore = defineStore('stock', {
  state: () => ({
    stockSectors: {
      /*
      - IT: Information Technology
      - F&B: Food and Beverage
      - Telecom: Telecommunication
      - Biotech: Biotechnology
      - Insurance: Insurance
      - Industry: Industrial
      - Automotive: Automotive
      - Energy: Energy
      - Steel: Steel Manufacturing
      - Electronics: Electronics and Semiconductor
      - Entertainment: Entertainment and Media
      - Construction: Construction and Infrastructure
      - Airline: Aviation
      - Logistics: Logistics and Transportation
      - Chemical: Chemical Manufacturing
      - Education: Education Services
      - Finance: Financial Services
      */
      '삼성에스디에스': 'IT', // 삼성에스디에스: IT
      '넥슨게임즈': 'IT', // 넥슨게임즈: IT
      '카카오': 'IT', // 카카오: IT
      'NAVER': 'IT', // NAVER: IT
      'CJ제일제당': 'F&B', // CJ제일제당: 식품
      '농심': 'F&B', // 농심: 식품
      '하이트진로': 'F&B', // 하이트진로: 음료
      '오뚜기': 'F&B', // 오뚜기: 식품
      'SK텔레콤': 'Telecom', // SK텔레콤: 통신
      'KT': 'Telecom', // KT: 통신
      '삼성바이오로직스': 'Biotech', // 삼성바이오로직스: 바이오
      '셀트리온': 'Biotech', // 셀트리온: 바이오
      '오리엔트바이오': 'Biotech', // 오리엔트바이오: 바이오
      '미래에셋생명': 'Insurance', // 미래에셋생명: 보험
      '삼보산업': 'Industry', // 삼보산업: 산업
      '한화생명': 'Insurance', // 한화생명: 보험
      '현대차': 'Automotive', // 현대차: 자동차
      '기아': 'Automotive', // 기아: 자동차
      '한국전력': 'Energy', // 한국전력: 에너지
      'POSCO홀딩스': 'Steel', // POSCO홀딩스: 철강
      '삼성전자': 'Electronics', // 삼성전자: 전자
      'SK하이닉스': 'Electronics', // SK하이닉스: 반도체
      'YG PLUS': 'Entertainment', // YG PLUS: 엔터테인먼트
      'JYP Ent.': 'Entertainment', // JYP Ent.: 엔터테인먼트
      '에스엠': 'Entertainment', // 에스엠: 엔터테인먼트
      'CJ CGV': 'Entertainment', // CJ CGV: 엔터테인먼트
      'GS건설': 'Construction', // GS건설: 건설
      'KD': 'Industry', // KD: 산업
      '대한항공': 'Airline', // 대한항공: 항공
      'CJ대한통운': 'Logistics', // CJ대한통운: 물류
      '제주항공': 'Airline', // 제주항공: 항공
      'SK이노베이션': 'Energy', // SK이노베이션: 에너지
      'S-Oil': 'Energy', // S-Oil: 에너지
      '롯데케미칼': 'Chemical', // 롯데케미칼: 화학
      'LG화학': 'Chemical', // LG화학: 화학
      '에스에너지': 'Energy', // 에스에너지: 에너지
      '메가스터디교육': 'Education', // 메가스터디교육: 교육
      '웅진씽크빅': 'Education', // 웅진씽크빅: 교육
      'KB금융': 'Finance', // KB금융: 금융
      '우리금융지주': 'Finance', // 우리금융지주: 금융
    },
    selectedStock: '삼성전자',
    stockMapping: {
      '삼성에스디에스': '018260',
      '넥슨게임즈': '225570',
      '카카오': '035720',
      'NAVER': '035420',
      'CJ제일제당': '097950',
      '농심': '004370',
      '하이트진로': '000080',
      '오뚜기': '389500',
      'SK텔레콤': '017670',
      'KT': '030200',
      '삼성바이오로직스': '207940',
      '셀트리온': '068270',
      '오리엔트바이오': '002630',
      '미래에셋생명': '085620',
      '삼보산업': '009620',
      '한화생명': '088350',
      '현대차': '005380',
      '기아': '000270',
      '한국전력': '015760',
      'POSCO홀딩스': '005490',
      '삼성전자': '005930',
      'SK하이닉스': '000660',
      'YG PLUS': '037270',
      'JYP Ent.': '035900',
      '에스엠': '041510',
      'CJ CGV': '079160',
      'GS건설': '006360',
      'KD': '044180',
      '대한항공': '003490',
      'CJ대한통운': '000120',
      '제주항공': '089590',
      'SK이노베이션': '096770',
      'S-Oil': '010950',
      '롯데케미칼': '011170',
      'LG화학': '051910',
      '에스에너지': '095910',
      '메가스터디교육': '215200',
      '웅진씽크빅': '095720',
      'KB금융': '105560',
      '우리금융지주': '316140',
    },
    tickers : [
      '018260', '225570', '035720', '035420', '097950', '004370', '000080',
      '389500', '017670', '030200', '207940', '068270', '002630', '085620',
      '009620', '088350', '005380', '000270', '015760', '005490', '005930',
      '000660', '037270', '035900', '041510', '079160', '006360', '044180',
      '003490', '000120', '089590', '096770', '010950', '011170', '051910',
      '095910', '215200', '095720', '105560', '316140'
    ]
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