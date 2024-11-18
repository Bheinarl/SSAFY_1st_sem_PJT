import pandas as pd
from django.http import JsonResponse
from FinanceDataReader import DataReader
from datetime import datetime, timedelta
from django.shortcuts import render

def get_stock_data(request):
    stock_codes = {
        '삼성전자': '005930',
        'SK하이닉스': '000660',
        '현대차': '005380',
        'POSCO홀딩스': '005490',
        '두산에너빌리티': '034020',
        '셀트리온': '068270',
        'NAVER': '035420',
        '기아': '000270',
        'LG에너지솔루션': '373220',
        '롯데케미칼': '011170'
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    stock_data = {}
    for name, code in stock_codes.items():
        df = DataReader(code, start=start_date, end=end_date)
        stock_data[name] = df.to_dict(orient='records')

    return JsonResponse(stock_data)
