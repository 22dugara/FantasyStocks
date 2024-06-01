import yfinance as yf
from portfolio.models import Stock, Portfolio, PortfolioAsset
from .models import Transaction
from decimal import Decimal

#Use some sort of finance org API to check for these
def validateStock(ticker):
    try:
        stock = yf.Ticker(ticker)
        # Check if the ticker has a valid market price
        if stock.info['regularMarketPrice'] is not None:
            return True
        else:
            return False
    except KeyError:
        return False

def getStockPrice(ticker):
    # For now, return a default price of 10 as a Decimal
    stock = yf.Ticker(ticker)
    price = stock.info['regularMarketPrice']
    return Decimal(str(price))

def validateTransaction(transaction_type, portfolio, stock, quantity, price):
    if transaction_type == 'buy':
        if portfolio.cash < quantity * price:
            return False, 'Not enough cash to complete the transaction.'
    elif transaction_type == 'sell':
        try:
            portfolio_asset = PortfolioAsset.objects.get(portfolio=portfolio, stock=stock)
        except PortfolioAsset.DoesNotExist:
            return False, 'You do not own this stock.'
        
        if portfolio_asset.quantity < quantity:
            return False, 'Not enough shares to complete the transaction.'
    return True, ''

def executeTrade(user, transaction_type, portfolio, stock, quantity, price):
    if transaction_type == 'buy':
        portfolio.cash -= quantity * price
        portfolio.save()

        portfolio_asset, created = PortfolioAsset.objects.get_or_create(
            portfolio=portfolio,
            stock=stock,
            defaults={'quantity': quantity, 'purchase_price': price}
        )
        if not created:
            portfolio_asset.quantity += quantity
            portfolio_asset.save()

    elif transaction_type == 'sell':
        portfolio_asset = PortfolioAsset.objects.get(portfolio=portfolio, stock=stock)
        portfolio_asset.quantity -= quantity
        portfolio_asset.save()
        if portfolio_asset.quantity == 0:
            portfolio_asset.delete()

        portfolio.cash += quantity * price
        portfolio.save()

    Transaction.objects.create(
        user=user,
        portfolio=portfolio,
        stock=stock,
        transaction_type=transaction_type,
        quantity=quantity,
        price=price
    )



#implement this. Check if a certain trade will violate the rules of a portfolio (ie. the diversity quotas)
def portfolioRulesCheck():
    return True