from django.http import JsonResponse
from .models import Stock
import FinanceDataReader as fdr
from datetime import datetime, timedelta

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
        print(data) # 디버깅 용도로 출력

        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
