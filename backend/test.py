import FinanceDataReader as fdr
import pandas as pd
import mplfinance as mpf
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# 한글 폰트 설정
font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows의 경우
fontprop = fm.FontProperties(fname=font_path, size=10)
plt.rc('font', family=fontprop.get_name())

# FinanceDataReader를 사용하여 주식 데이터 가져오기
code = '005930'
df = fdr.DataReader(code)

# 최근 5일간의 데이터만 선택
df = df.tail(30)

# 데이터프레임의 인덱스를 날짜로 설정
df.index.name = 'Date'

# 캔들스틱 색상 설정
mc = mpf.make_marketcolors(up='r', down='b', edge='inherit', wick='inherit', volume='inherit')
s = mpf.make_mpf_style(marketcolors=mc)

# 캔들스틱 차트 그리기 (거래량 차트 생략)
mpf.plot(df, type='candle', style=s, title='Samsung Electronics Stock', ylabel='Price', datetime_format='%y-%m-%d')