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
    if request.method == 'POST':
        data = json.loads(request.body)
        CurrencyAlert.objects.create(
            user=request.user,
            currency=data['currency'],
            target_rate=data['target_rate']
        )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

def get_exchange_rate(request):
    # 환율 API URL 및 API 키 (예시: 한국 수출입은행 API 사용)
    api_url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXCHANGE_RATE_API_KEY}&data=AP01"

    try:
        # API 호출
        response = requests.get(api_url)
        response.raise_for_status()  # 오류 발생 시 예외 처리
        data = response.json()
        return JsonResponse(data, safe=False)  # 리스트 형태일 수 있으므로 safe=False 추가
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': '환율 데이터를 가져오는 중 오류가 발생했습니다.'}, status=500)