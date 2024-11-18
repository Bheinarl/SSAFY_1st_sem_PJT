from django.http import JsonResponse
from .models import Stock
import FinanceDataReader as fdr

def stock_data(request, ticker):
    try:
        start_date = '2024-07-01'
        end_date = '2024-07-14'

        df = fdr.DataReader(ticker, start=start_date, end=end_date)
        # print(df)  // 디버깅 용도로 출력
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

        # 데이터베이스에 저장
        for index, row in df.iterrows():
            Stock.objects.update_or_create(
                ticker=ticker,
                date=row['Date'],
                defaults={
                    # 'close_price': row['Close'],
                    'open_price': row['Open'],
                    }
            )

        # 데이터 조회
        stocks = Stock.objects.filter(ticker=ticker, date__range=[start_date, end_date])
        data = list(stocks.values('date', 'open_price'))
        # print(data) // 디버깅 용도로 출력

        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
