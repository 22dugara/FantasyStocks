from django.contrib import admin
from .models import Stock, FixedIncomeSecurity, Portfolio, PortfolioAsset

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'category')
    search_fields = ('name', 'ticker')

@admin.register(FixedIncomeSecurity)
class FixedIncomeSecurityAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'maturity_date', 'interest_rate')
    search_fields = ('name', 'ticker')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user__username', 'name')

@admin.register(PortfolioAsset)
class PortfolioAssetAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'asset', 'quantity', 'purchase_price')
    search_fields = ('portfolio__name', 'asset__name')
