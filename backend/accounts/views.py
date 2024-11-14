# accounts/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
import json
from .models import UserProfile, CurrencyAlert
from .forms import UserProfileForm, SignUpForm
from django.conf import settings
import requests
from datetime import datetime, timedelta

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('profile_setup')  # 회원가입 후 프로필 설정 페이지로 이동
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def profile_setup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('investment_analysis')
    else:
        form = UserProfileForm()
    return render(request, 'accounts/profile_setup.html', {'form': form})

def investment_analysis(request):
    profile = UserProfile.objects.get(user=request.user)
    investment_tendency = profile.investment_tendency
    recommended_strategy = "안정형 포트폴리오" if investment_tendency == "stable" else (
        "공격형 포트폴리오" if investment_tendency == "aggressive" else "균형형 포트폴리오"
    )
    return render(request, 'accounts/investment_analysis.html', {'strategy': recommended_strategy})

@csrf_exempt
def set_alert(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            
            # CurrencyAlert 모델에 알림 정보 저장
            CurrencyAlert.objects.create(
                user=request.user if request.user.is_authenticated else None,  # 로그인하지 않은 사용자는 None으로 설정
                currency=data['currency'],
                target_rate=data['target_rate']
            )
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({'status': 'fail'}, status=400)
    
    except Exception as e:
        print(f"알림 설정 중 오류 발생: {e}")
        return JsonResponse({'error': '알림 설정 중 오류가 발생했습니다.'}, status=500)

def check_exchange_rate(request):
    print("check_exchange_rate 함수 호출됨")
    print(f'리퀘스트 : {request.GET}')
    currency = request.GET.get('currency')
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"
    # 오전 11시 이전이라면 오늘을 기준으로 어제 데이터 사용
    if datetime.now().hour < 11:
        yesterday = datetime.now() - timedelta(days=1)
        api_url += f"&searchdate={yesterday.strftime('%Y%m%d')}"
    
    try:
        response = requests.get(api_url, verify=False)  # SSL 검증 비활성화
        response.raise_for_status()
        
        data = response.json()
        print(currency)
        # USD 환율 데이터 추출
        currency_data = next((item for item in data if item['cur_unit'] == currency), None)
        if not currency_data:
            return JsonResponse({'error': '환율 데이터를 찾을 수 없습니다.'}, status=500)

        # 현재 환율
        current_rate = float(currency_data['deal_bas_r'].replace(',', ''))
        print(f"현재 {currency} 환율: {current_rate}")

        # 가장 최근에 설정된 알림을 기준으로 목표 환율 확인
        alert = CurrencyAlert.objects.filter(currency=currency).order_by('-created_at').first()
        print(f"알림 설정: {alert}")

        # 알림 설정이 있고, 현재 환율이 목표 환율 이하인 경우 알림 반환
        if alert and current_rate <= alert.target_rate:
            return JsonResponse({'alert': True, 'current_rate': current_rate})
        else:
            return JsonResponse({'alert': False, 'current_rate': current_rate})

    except Exception as e:
        print(f"기타 오류 발생: {e}")
        return JsonResponse({'error': '알 수 없는 오류가 발생했습니다.'}, status=500)

'''
def check_exchange_rate(request):
    print("check_exchange_rate 함수 호출됨")
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"
    print(f"API URL: {api_url}")
    
    try:
        response = requests.get(api_url, verify=False)  # SSL 검증 비활성화
        print(f"API 응답 상태 코드: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()
        print(f"API에서 받은 데이터: {data}")

        usd_data = next((item for item in data if item['cur_unit'] == 'USD'), None)
        if not usd_data:
            print("환율 데이터를 찾을 수 없습니다.")
            return JsonResponse({'error': '환율 데이터를 찾을 수 없습니다.'}, status=500)

        # 쉼표 제거 후 float 변환
        current_rate = float(usd_data['deal_bas_r'].replace(',', ''))
        print(f"현재 USD 환율: {current_rate}")

        # 인증되지 않은 사용자도 사용할 수 있도록 alert 조회 로직을 조건부로 변경
        alert = None
        if request.user.is_authenticated:
            alert = CurrencyAlert.objects.filter(user=request.user, currency="KRW").first()
            print(f"사용자 알림 설정: {alert}")

        if alert and current_rate <= alert.target_rate:
            return JsonResponse({'alert': True, 'current_rate': current_rate})
        else:
            return JsonResponse({'alert': False, 'current_rate': current_rate})

    except requests.exceptions.HTTPError as e:
        print(f"HTTP 오류 발생: {e}")
        return JsonResponse({'error': '환율 데이터를 가져오는 중 HTTP 오류가 발생했습니다.'}, status=500)
    except requests.exceptions.RequestException as e:
        print(f"API 요청 오류 발생: {e}")
        return JsonResponse({'error': '환율 데이터를 가져오는 중 API 요청 오류가 발생했습니다.'}, status=500)
    except Exception as e:
        print(f"기타 오류 발생: {e}")
        return JsonResponse({'error': '알 수 없는 오류가 발생했습니다.'}, status=500)
'''

def get_exchange_rate(request):
    # 환율 API URL 및 API 키 (예시: 한국 수출입은행 API 사용)
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"
    # 오전 11시 이전이라면 오늘을 기준으로 어제 데이터 사용
    if datetime.now().hour < 11:
        yesterday = datetime.now() - timedelta(days=1)
        api_url += f"&searchdate={yesterday.strftime('%Y%m%d')}"
    
    try:
        # API 호출
        response = requests.get(api_url)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        data = response.json()
        return JsonResponse(data, safe=False)  # 리스트 형태일 수 있으므로 safe=False 추가
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': '환율 데이터를 가져오는 중 오류가 발생했습니다.'}, status=500)