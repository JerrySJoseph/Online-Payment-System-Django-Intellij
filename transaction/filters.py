from django_filters import FilterSet
from .models import Transaction
from django import forms
from wallet.models import Currency

class TransactionFilter(FilterSet):
    type=forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'class': 'form-select'}
    ))
    class Meta:
        model=Transaction
        fields=['type','currency','datetime']