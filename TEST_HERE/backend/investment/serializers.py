from rest_framework import serializers
from .models import Investment, InvestmentAnalysis

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = ['id', 'user', 'asset_type', 'amount', 'created_at']

class InvestmentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentAnalysis
        fields = ['user', 'conservative_ratio', 'aggressive_ratio', 'created_at']
