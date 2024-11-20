import requests
from bs4 import BeautifulSoup

# HTTP 요청 헤더 설정
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

# 크롤링할 URL
url = "https://finance.naver.com/news/mainnews.naver?date=2020-01-02"

# HTTP 요청 보내기
response = requests.get(url, headers=headers)

# HTML 파싱
soup = BeautifulSoup(response.text, 'lxml')

# 뉴스 제목 추출
# 클래스 없이 크롤링 하는 방법 구현
news_titles = [title.text.strip() for title in soup.select('dd.articleSubject a')]

# 결과 출력
for one_of_news_title in news_titles :
    print(one_of_news_title)
# print(news_titles)
