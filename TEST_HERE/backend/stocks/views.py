from django.http import JsonResponse
from .models import Stock, NewsHeadline
import FinanceDataReader as fdr
from datetime import datetime, timedelta
from django.db import transaction
import concurrent.futures
import random

import requests
from bs4 import BeautifulSoup

def fetch_news(request):
    try:
        start_date_str = request.GET.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

        # 날짜를 'YYYYMMDD' 형식으로 변환
        date_str = start_date.strftime('%Y%m%d')

        # URL에 날짜 파라미터 추가
        # url = f"https://finance.naver.com/news/mainnews.naver?date={date_str}"
        url = f"https://finance.naver.com/news/news_list.naver?mode=LSS2D&section_id=101&section_id2=258&date={date_str}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 뉴스 제목 추출
        titles = []
        for title in soup.select('dd.articleSubject a'):
            titles.append(title.text.strip())
            if len(titles) == 10:  # 10개까지만 가져옴
                break
        # print(titles)  # 디버깅용으로 출력

        return JsonResponse({'status': 'success', 'message': 'News headlines saved successfully', 'data': titles}, status=200)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

def generate_random_date(request):
    try:
        start_year = random.randrange(2020, 2024)  # 2020~2023 까지 랜덤
        start_month = random.randrange(1, 13)  # 1~12 까지 랜덤
        if start_month in [1, 3, 5, 7, 8, 10, 12]:
            start_date = random.randrange(1, 32)  # 1~31 까지 랜덤
        elif start_month in [4, 6, 9, 11]:
            start_date = random.randrange(1, 31)  # 1~30 까지 랜덤
        else:  # 2월
            start_date = random.randrange(1, 29)  # 1~28 까지 랜덤

        temp = f"{start_year}-{start_month:02d}-{start_date:02d}"
        start_date = datetime.strptime(temp, '%Y-%m-%d')
        return JsonResponse({'status': 'success', 'start_date': start_date.strftime('%Y-%m-%d')})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# def stock_data(request):
#     try:
#         tickers = [
#             '018260', '225570', '035720', '035420', '097950', '004370', '000080',
#             '389500', '017670', '030200', '207940', '068270', '002630', '085620',
#             '009620', '088350', '005380', '000270', '015760', '005490', '005930',
#             '000660', '037270', '035900', '041510', '079160', '006360', '044180',
#             '003490', '000120', '089590', '096770', '010950', '011170', '051910',
#             '095910', '215200', '095720', '105560', '316140'
#         ]

#         start_date_str = request.GET.get('start_date')
#         start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
#         end_date = start_date + timedelta(days=9)  # 10일간의 데이터를 가져오기 위해

#         result_data = {}

#         for ticker in tickers:
#             data = []
#             while len(data) < 10:
#                 stocks = Stock.objects.filter(ticker=ticker, date__range=[start_date, end_date])

#                 for stock in stocks:
#                     # 각 Stock에 해당하는 NewsHeadline을 가져와서 추가
#                     news = NewsHeadline.objects.filter(date=stock.date)  # 해당 날짜에 맞는 뉴스 제목
#                     news_data = [{'headline': nh.headline} for nh in news]  # 필요한 데이터만 추출

#                     data.append({
#                         'date': stock.date,
#                         'open_price': stock.open_price,
#                         'close_price': stock.close_price,
#                         'news': news_data  # 뉴스 제목들
#                     })
                    
#                 # 날짜를 하루씩 증가
#                 end_date += timedelta(days=1)

#             # 10개 이상의 데이터가 있으면 10개로 자름
#             if len(data) > 10:
#                 data = data[:10]
            
#             result_data[ticker] = data
        
#         return JsonResponse({'status': 'success', 'data': result_data})

#     except Exception as e:
#         return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def stock_data(request, ticker):
    try:
        start_date_str = request.GET.get('start_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = start_date + timedelta(days=9)  # 10일간의 데이터를 가져오기 위해

        data = []
        while len(data) < 10:
            stocks = Stock.objects.filter(ticker=ticker, date__range=[start_date, end_date])
            data = list(stocks.values('date', 'open_price', 'close_price'))
            end_date += timedelta(days=1)

        if len(data) > 10:
            data = data[:10]
        
        return JsonResponse({'status': 'success', 'data': data})
        ###############

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

def fetch_and_save_ticker_data(ticker, start_date, end_date):
    print("Fetching data for", ticker) # 디버깅 용도로 출력
    try:
        # 데이터 가져오기
        df = fdr.DataReader(ticker, start=start_date, end=end_date)
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        
        # 데이터 준비
        bulk_data = [
            Stock(
                ticker=ticker,
                date=row['Date'],
                open_price=row['Open'],
                close_price=row['Close'],
            )
            for _, row in df.iterrows()
        ]
        return bulk_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return []
        
def stock_list(request):
    print("stock_list") # 디버깅 용도로 출력
    try:
        # Stock에 데이터가 존재하면 return하는 코드
        if Stock.objects.exists():
            stocks = Stock.objects.all().values('ticker').distinct()
            return JsonResponse({'status': 'success', 'data': list(stocks)})
        
        # 데이터 수집
        tickers = [
            '018260', '225570', '035720', '035420', '097950', '004370', '000080',
            '389500', '017670', '030200', '207940', '068270', '002630', '085620',
            '009620', '088350', '005380', '000270', '015760', '005490', '005930',
            '000660', '037270', '035900', '041510', '079160', '006360', '044180',
            '003490', '000120', '089590', '096770', '010950', '011170', '051910',
            '095910', '215200', '095720', '105560', '316140'
        ]
        start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2024-01-31', '%Y-%m-%d')

        # 병렬 처리로 데이터 수집
        all_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_ticker = {executor.submit(fetch_and_save_ticker_data, ticker, start_date, end_date): ticker for ticker in tickers}
            for future in concurrent.futures.as_completed(future_to_ticker):
                result = future.result()
                if result:
                    all_data.extend(result)

        # 데이터베이스에 저장
        with transaction.atomic():
            Stock.objects.bulk_create(all_data, ignore_conflicts=True)

        return JsonResponse({'status': 'success', 'message': 'Data saved successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)