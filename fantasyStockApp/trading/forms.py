from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    transaction_type = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES)
    ticker = forms.CharField(max_length=10)
    quantity = forms.IntegerField()

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'ticker', 'quantity']
