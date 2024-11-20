from django.http import JsonResponse
from .models import Stock
import FinanceDataReader as fdr
from datetime import datetime, timedelta
from django.db import transaction
import concurrent.futures

def stock_data(request, ticker):
    try:
        start_date = datetime.strptime('2024-09-16', '%Y-%m-%d')
        end_date = start_date

        data = []
        while len(data) < 10:
            df = fdr.DataReader(ticker, start=start_date, end=end_date)
            df = df.reset_index()
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

            # 데이터베이스에 저장
            for index, row in df.iterrows():
                Stock.objects.update_or_create(
                    ticker=ticker,
                    date=row['Date'],
                    defaults={
                        'open_price': row['Open'],
                        'close_price': row['Close'],
                    }
                )

            # 데이터 조회
            stocks = Stock.objects.filter(ticker=ticker, date__range=[start_date, end_date])
            data = list(stocks.values('date', 'open_price', 'close_price'))

            # end_date 하루 증가
            end_date += timedelta(days=1)

        # data의 원소 개수가 10개가 되도록 조정
        if len(data) > 10:
            data = data[:10]
        # print(data) # 디버깅 용도로 출력

        return JsonResponse({'status': 'success', 'data': data})
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