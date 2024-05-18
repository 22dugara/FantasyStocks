from django.contrib import admin
from .models import Stock, Portfolio, PortfolioAsset

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'ticker', 'category')
    search_fields = ('name', 'ticker')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user__username', 'name')

@admin.register(PortfolioAsset)
class PortfolioAssetAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'quantity', 'purchase_price')
    search_fields = ('portfolio__name', 'stock__name')

