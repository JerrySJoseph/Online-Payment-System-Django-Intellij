from django import forms
from account.models import Currency


# A custom validator to limit transactions of large amounts
def large_amount_validator(amount):
    if int(amount)>10000:
        raise forms.ValidationError('You cannot add more than 10000 in one transaction')

# Form to add money to user wallet
class AddMoneyForm(forms.Form):
    amount=forms.DecimalField(decimal_places=2,max_digits=20,widget=forms.TextInput(
        attrs={'placeholder': 'Eg: 2,000,000.00'}),validators=[large_amount_validator])
    

# form to change default currency of user wallet
class ChangeCurrencyForm(forms.Form):
    currency=forms.ChoiceField(choices=Currency.choices,required=True,widget=forms.Select(
        attrs={'placeholder': 'Default Currency'},
    ))

    def __init__(self,current_currency:Currency,*args, **kwargs):
        super(ChangeCurrencyForm, self).__init__(*args, **kwargs)
        # set initial currency to current currency
        self.fields['currency'].initial=current_currency
    