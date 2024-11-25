from django.db import models

class InvestmentAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investor_type = models.CharField(max_length=50)
    risk_level = models.FloatField()
    trade_count = models.IntegerField()
    preferred_sectors = models.JSONField()
    final_value = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)