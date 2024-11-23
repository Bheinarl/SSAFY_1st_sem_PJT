from django.db import models
    
class NewsHeadline(models.Model):
    date = models.DateField()
    headline = models.CharField(max_length=200)

    def __str__(self):
        return self.headline


class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()

    def __str__(self):
        return f"{self.ticker} - {self.date}"