from django.http import JsonResponse
import FinanceDataReader as fdr

def stock_data(request, ticker):
    try:
        # 시작 날짜와 종료 날짜를 GET 요청에서 가져옴
        start_date = request.GET.get('start', '2023-01-01')
        end_date = request.GET.get('end', '2023-12-31')

        # finance-datareader로 주식 데이터 가져오기
        df = fdr.DataReader(ticker, start=start_date, end=end_date)
        df = df.reset_index()
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')  # 날짜를 문자열로 변환
        data = df[['Date', 'Close']].to_dict(orient='records')  # 필요한 데이터만 변환

        return JsonResponse({'status': 'success', 'data': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# import pandas as pd
# from django.http import JsonResponse
# from FinanceDataReader import DataReader
# from datetime import datetime, timedelta
# from django.shortcuts import render

# def get_stock_data(request):
#     stock_codes = {
#         '삼성전자': '005930',
#         'SK하이닉스': '000660',
#         '현대차': '005380',
#         'POSCO홀딩스': '005490',
#         '두산에너빌리티': '034020',
#         '셀트리온': '068270',
#         'NAVER': '035420',
#         '기아': '000270',
#         'LG에너지솔루션': '373220',
#         '롯데케미칼': '011170'
#     }

#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=365)

#     stock_data = {}
#     for name, code in stock_codes.items():
#         df = DataReader(code, start=start_date, end=end_date)
#         stock_data[name] = df.to_dict(orient='records')

#     return JsonResponse(stock_data)
