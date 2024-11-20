# from django.http import JsonResponse

# import requests
# from bs4 import BeautifulSoup
# from django.http import JsonResponse

# def fetch_news(request):
#     try:
#         url = "https://finance.naver.com/news/mainnews.naver?date=2020-01-01"
#         response = requests.get(url)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # 뉴스 제목 추출
#         titles = [
#             title.text.strip()
#             for title in soup.select('dd.articleSubject a')
#         ]

#         return JsonResponse({'status': 'success', 'titles': titles}, status=200)
#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup

def fetch_news(request):
    try:
        # 요청에서 날짜 파라미터 가져오기
        date = request.GET.get('date', '2020-01-01')  # 기본값으로 2020-01-01 설정
        
        # URL에 날짜 파라미터 추가
        url = f"https://finance.naver.com/news/mainnews.naver?date={date}"
        
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 제목 추출
        titles = [
            title.text.strip()
            for title in soup.select('dd.articleSubject a')
        ]

        return JsonResponse({'status': 'success', 'titles': titles}, status=200)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)