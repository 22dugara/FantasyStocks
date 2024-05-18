from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TransactionForm
from .models import Transaction
from portfolio.models import Stock, Portfolio
from .helpers import validateStock, getStockPrice, validateTransaction, executeTrade

@login_required
def transact(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction_type = form.cleaned_data['transaction_type']
            ticker = form.cleaned_data['ticker']
            quantity = form.cleaned_data['quantity']
            price = getStockPrice(ticker)  # Get the stock price using the helper function

            if not validateStock(ticker):
                messages.error(request, 'Invalid stock ticker.')
                return redirect('transact')

            stock, created = Stock.objects.get_or_create(ticker=ticker, defaults={'name': ticker, 'category': 'other'})
            
            portfolio = Portfolio.objects.get(user=request.user)

            is_valid, error_message = validateTransaction(transaction_type, portfolio, stock, quantity, price)
            if not is_valid:
                messages.error(request, error_message)
                return redirect('transact')

            executeTrade(request.user, transaction_type, portfolio, stock, quantity, price)

            messages.success(request, 'Transaction successful.')
            return redirect('portfolio_management')
    else:
        form = TransactionForm()

    return render(request, 'transact.html', {'form': form})
