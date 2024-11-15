from rest_framework import viewsets
from .models import Investment, InvestmentAnalysis
from .serializers import InvestmentSerializer, InvestmentAnalysisSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

class InvestmentAnalysisViewSet(viewsets.ModelViewSet):
    queryset = InvestmentAnalysis.objects.all()
    serializer_class = InvestmentAnalysisSerializer
