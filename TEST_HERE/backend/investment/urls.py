from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestmentViewSet, InvestmentAnalysisViewSet

router = DefaultRouter()
router.register(r'investments', InvestmentViewSet)
router.register(r'investment-analysis', InvestmentAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
