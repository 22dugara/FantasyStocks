from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Asset(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Stock(Asset):
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
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return f"{self.name} ({self.ticker}) - {self.get_category_display()}"


class FixedIncomeSecurity(Asset):
    maturity_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.ticker}) - Matures on {self.maturity_date}"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

class PortfolioAsset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='assets')
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    asset = GenericForeignKey('content_type', 'object_id')
    
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} units of {self.asset.name} in {self.portfolio.name}"

