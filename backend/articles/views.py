# # articles/views.py

# from django.http import JsonResponse
# from .models import LocationBasedRecommendation

# def location_recommendation(request):
#     recommendation = LocationBasedRecommendation.objects.filter(user=request.user).last()
#     return JsonResponse({'recommended_product': recommendation.recommended_product if recommendation else "추천 상품 없음"})


# # articles/views.py

# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from .models import LocationBasedRecommendation

# @login_required
# def location_recommendation(request):
#     recommendation = LocationBasedRecommendation.objects.filter(user=request.user).last()
#     return JsonResponse({'recommended_product': recommendation.recommended_product if recommendation else "추천 상품 없음"})


# articles/views.py

from django.http import JsonResponse
from .models import LocationBasedRecommendation

def location_recommendation(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=403)

    recommendation = LocationBasedRecommendation.objects.filter(user=request.user).last()
    return JsonResponse({'recommended_product': recommendation.recommended_product if recommendation else "추천 상품 없음"})
