# README 📘  

## 📌 프로젝트 소개 🏦  
- **모의 투자 플랫폼**은 금융 데이터 기반으로 사용자에게 투자 학습과 가상 자산 운용 기회를 제공합니다.  
개인 맞춤형 금융 상품 추천과 투자 성향 분석을 통해 사용자에게 맞는 금융 상품을 추천하는 웹 애플리케이션입니다.  
---

## 🙌 팀 구성 및 역할
- 기획: 곽동연, 임현주
- 프론트엔드 개발: 곽동연, 임현주
- 백엔드 개발: 곽동연, 임현주
- 데이터 처리 및 크롤링: 곽동연, 임현주

---

## 설계 내용 및 실제 구현 정도 🔧  

### 초기 아이디어 💡
- 은행에서 특정 금융상품에 가입하기 전, 고객이 설문조사를 통해 투자 성향을 분석하고 가입 여부를 결정하도록 하는 방식에서 착안.
- 기존의 투자 성향 설문은 고객이 자발적으로 응답하는 자기보고(self-report) 방식으로, 응답자가 의도적으로 답변을 조작하거나 자신의 실제 성향과 다르게 표현할 수 있다는 한계가 존재.

### 프로젝트 목표
- 게임 플레이를 통한 자연스러운 사용자 행동 분석을 통해 이러한 한계를 극복하고자 함.
- 사용자는 가상 투자 시나리오에서 의사결정을 내리며, 우리는 이 과정에서 수집된 데이터를 기반으로 사용자의 실제 투자 성향을 보다 정확하게 파악.
- 이를 통해 의도적인 응답 왜곡을 최소화하고, 사용자에게 맞춤형 금융 상품을 추천할 수 있음.

### ✨ 설계 목표
1. **모의 투자 게임** 💸  
   - 공공데이터포털 및 네이버 증권 데이터, 뉴스 데이터를 활용한 실시간 투자 시뮬레이션.
   - **실제** 주식 데이터와 해당 일자에 맞는 뉴스 데이터를 연동함으로써 모의 투자 게임의 효용성을 높임

2. **투자 성향 분석 및 금융 상품 추천** 💡  
   - 사용자 데이터를 기반으로 투자 성향 분석 및 맞춤형 상품 추천.

3. **커뮤니티 기능** 🗨️  
   - 사용자 간 소통과 기록 공유를 위한 게시판 제공.
   - 금융 상품 후기 공유, 비슷한 투자 성향을 가진 사용자의 추천, 모의 투자 게임 점수 향상 방법 공유 등을 통해 **커뮤니티 활성화**

4. 환율 계산기
   - **외국 주식 시장에 대한 모의 투자 지원을 위해** 환율 계산기 설계.

5. **환율 알림 기능** 🔔  
   - 환율 계산기에 **환율 알림 기능**을 추가하여 사용자가 설정한 환율 조건에 도달하면 즉시 알림을 제공
   - **환율 변동에 따른 중요한 시점을 즉시 알려 해외 주식에 대한 투자 결정을 용이하게** 하여, 사용자가 효율적으로 투자 기회를 포착할 수 있도록 지원

6. 카카오맵 지도 API 활용
   - 사용자 현재 위치를 기반으로 한 지도 검색 기능을 구현
   - 추천 상품에 관심이 있을 경우, 사용자가 이동 중에 해당 은행을 방문할 수 있도록 "당신이 마음에 든 그 상품! 집가는 길에 바로 가입 가능해요"와 같은 메시지를 제공
   - **특정 키워드를 클릭하면 자동으로 검색되도록 기능을 구현**하여 편의성을 높임

7. 프로필 및 랭킹 기능
   - **상위 10위**의 랭킹(리더보드)을 제공하여 사용자 간의 경쟁 심리를 자극하고, 이를 통해 사이트 이용을 활성화
   - 사용자 프로필에 자신의 투자 성향이나 유형을 명시함으로써 재미 요소를 부여
   -  랭킹과 프로필 기능을 통해 사용자들 간의 상호 작용을 촉진하고, 커뮤니티 참여를 증진


### 🎯 실제 구현 정도 
- **미완성 기능:**  
  - 해외 주식 데이터 연동
  - 환율 데이터 수신 후 **실시간** 알림 기능
- 완성 기능 :
  - 그 외 나머지 기능  

---

## 데이터베이스 모델링 (ERD) 🗂️  

### 주요 엔티티  
```plaintext
CustomUser
├── CurrencyAlert (1:N)
├── Post (1:N)
│   └── liked_users (M:N with CustomUser)
└── InvestmentTransaction (1:N)
└── FundRecommendation (1:N)
NewsHeadLine
Stock
Location
DepositProduct
SavingProduct
FundProduct
```

---

## 금융상품 추천 알고리즘에 대한 기술적 설명 🤖  

### 📔 참고 논문에서의 아이디어
1. 주식 투자 종목 수와 위험 분산 효과
  - 본능적 투자자: 긍정적 메시지 프레이밍에 노출되었을 때, 효과적으로 투자 종목을 분산하는 경향을 보였습니다.
  - 감정적 및 이성적 투자자: 부정적 메시지 프레이밍에 노출되었을 때, 효과적인 분산 투자를 하는 경향이 있었습니다.
2. 위험 투자 자산 포트폴리오 중 주식 투자 비율
  - 본능적 투자자: 긍정적 메시지 프레이밍에 노출되었을 때, 더 높은 위험 수용 능력(risk tolerance)을 보였습니다.
  - 감정적 및 이성적 투자자: 부정적 메시지 프레이밍에 노출되었을 때, 더 높은 위험 수용 능력을 나타냈습니다.
3. 금융 거래를 이용한 주식 투자 부채 비율
  - 감정적 투자자: 긍정적 메시지 프레이밍에 노출되었을 때, 더 높은 위험 수용 능력을 보였습니다.
  - 본능적 및 이성적 투자자: 부정적 메시지 프레이밍에 노출되었을 때, 더 높은 위험 수용 능력을 나타냈습니다.
4. 위험 관리 행동 측정
  - 재무 자산 소유 비율: 총 자산 중 재무 자산을 얼마나 소유하고 있는지의 비율을 통해 재무 위험 행동을 측정했습니다.
  - 위험 회피에 대한 주관적 태도: 주관적인 위험 평가로 투자자의 위험 회피 성향을 측정했습니다.

### 📊 투자 성향 분석  
사용자의 투자 활동 데이터를 기반으로 투자 성향을 아래의 네 가지 유형으로 분류합니다:  
1. **안정 추구형**   
2. **균형 투자형**   
3. **공격 투자형**   
4. **투기형**

#### 분석 기준과 가중치  
| **기준**          | **가중치** |  
|------------------|----------|  
| 거래 빈도         | 30%       |  
| 보유 기간         | 30%       |  
| 자산 분배율       | 20%       |  
| 섹터 다양성       | 10%       |  
| 종목 분산도       | 10%       |  

### 🏦 금융 상품 추천  
1. **펀드 추천:**  
   - 공공데이터포털 API를 활용해 사용자의 투자 유형별로 맞춤형 펀드를 추천합니다.  
   - 펀드 이름을 클릭하면 상세 정보를 제공하는 외부 사이트로 이동합니다.  
2. **정기예금/적금 추천:**  
   - 금융감독원 금융상품통합비교공시 데이터를 기반으로 적합한 상품을 추천합니다.  
   - 사용자의 현재 위치를 기반으로 주변 은행을 지도에 표시.  

---

## 서비스 대표 기능 🌟  

### 💸 모의 투자 게임  
- 실시간 데이터를 기반으로 한 가상 자산 운용.  
- 투자 성향 분석 자료로 활용.  

### 🔔 환율 계산기  
- 한국 수출입은행 OpenAPI를 활용하여 실시간 환율 데이터 제공.  
- 알림 설정 기능: 설정값 이하로 환율이 떨어지면 알림 발생.  

### 🏦 금융 상품 추천  
- 투자 성향에 맞는 금융 상품 추천.  
- 펀드, 정기예금, 적금 등 다양한 상품 포함.  

### 🗨️ 게시판  
- 투자 전략과 기록 공유를 위한 커뮤니티 공간.  
- 게시글 생성, 수정, 삭제, 좋아요 기능 제공.  

---


## 🛠️ 기술 스택  

### **Frontend**  
- Vue.js  
- Chart.js (차트 시각화)  

### **Backend**  
- Django REST Framework  
- dj_rest_auth (회원 인증 및 토큰 관리)  

### **Database**  
- SQLite  

### **API**  
- 공공데이터포털 API  
- 한국 수출입은행 OpenAPI  
- 금융감독원 금융상품통합비교공시  

### **Web Scraping**  
- BeautifulSoup (네이버 증권 실시간 속보 크롤링)  

--- 

## 느낀 점, 후기 ✍️  

### 😊 배운 점
- **실시간 데이터 활용:**  
  공공데이터포털 API와 웹 크롤링을 통해 실시간 데이터를 제공하는 기술을 익혔습니다.  
- **백엔드-프론트엔드 연동:**  
  Django와 Vue.js를 연결하며 실시간 데이터 반영 및 API 설계의 중요성을 배웠습니다.
- **Git 활용 능력 향상:**  
  Git과 GitHub를 활용한 협업 및 버전 관리 방법을 익히며 코드 관리의 중요성을 배웠습니다.

### 🚀 앞으로의 계획  
1. 사용자의 투자 성향 모델 개선: **뉴스 데이터** 속 긍정적 메시지(예: "성장성 높음")와 부정적 메시지(예: "손실 가능성 있음")에 대한 투자자의 거래 변화를 파악하여 모델 개선할 계획입니다.
2. 해외 주식 데이터 연동: 해외 주식 데이터를 수집하여 환율 계산기를 활용한 손익 계산 기능을 완성할 예정입니다.
3. 카카오톡 알림 기능 구현: 카카오톡 API를 연동해 사용자가 설정한 기준값 이하로 환율이 떨어질 경우 실시간 메시지를 전송하는 기능을 추가할 계획입니다.
4. UI/UX 개선: 사용자 피드백을 반영해 더 직관적이고 편리한 인터페이스를 제공하도록 디자인을 개선할 계획입니다.
5. 데이터 최적화: 환율 데이터를 더 효율적으로 수집하고 처리하여 앱의 속도와 안정성을 개선할 예정입니다.
6. 배포: 완성된 기능을 안정적으로 배포할 예정입니다.
