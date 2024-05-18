from django.db import models
from django.contrib.auth.models import User
from leagues.models import League

class Stock(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('energy', 'Energy'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('consumer', 'Consumer'),
        ('utilities', 'Utilities'),
        ('realestate', 'Real Estate'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return f"{self.name} ({self.ticker}) - {self.get_category_display()}"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=100000.00)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} units of {self.stock.name} in {self.portfolio.name}"







"""
class Asset(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name"""

"""class FixedIncomeSecurity(Asset):
    maturity_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.ticker}) - Matures on {self.maturity_date}" """""
