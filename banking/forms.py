from django import forms
from django.db import models
from wallet.models import Wallet
from account.models import Currency
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from decimal import Decimal
from iam.api.register import check_email_exists, check_username_exists
from .utils.search import search_with_identifier
from .utils.transfers import balance_check
from .utils.wallet import get_wallet_profile_by_id
from .utils.bank_account import add_bank_account,edit_bank_account,remove_bank_account
from wallet.utils.exceptions.TransactionException import TransferException



#validate email field
def email_validator(email):
    #make sure the given email doesn't already exists in the database
    if not check_email_exists(email=email):
        raise forms.ValidationError('A user exists with this email id.')

#validate username field
def username_validator(username):
    #make sure the given username doesn't already exists in the database
    if not check_username_exists(username=username):
        raise forms.ValidationError(_('A user exists with username : %(invalid_username)s'), params={
            'invalid_username': username
        })


class RequestForm(forms.Form):
    identifier=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'username, email, firstname or lastname'}), required=True,validators=[])
    amount=forms.DecimalField(decimal_places=2,max_digits=20,widget=forms.TextInput(
        attrs={'placeholder': 'Eg: 2,000,000.00'}))
    currency=forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'username, email, firstname or lastname'}
    ))

def notEmptyValidator(identifier):
    if identifier is None or len(identifier)<=0:
        raise forms.ValidationError('This field cannot be empty')

class SearchForm(forms.Form):
    tag=forms.CharField(widget=forms.HiddenInput(attrs={'value':'search'}),required=True)
    identifier=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search your recipient by name, email or userid'}), required=True,validators=[notEmptyValidator],label=None)
    
    def search(self):
        string=self.cleaned_data['identifier']
        results=search_with_identifier(string)
        if len(results)<=0:
            self.add_error('identifier',forms.ValidationError('We couldnot find any user having similar name, email or username'))
        return results


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    

class SendDetailForm(forms.Form):
       
    amount=forms.DecimalField(decimal_places=2,widget=forms.NumberInput(
        attrs={'placeholder': 'Eg: $200.00',
               'type':'number'
               }), required=True,validators=[],label=None)
    currency=forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               }
    ))
   
    wallet=None
    #sender=None
    def __init__(self,sender,*args, **kwargs):
        
        super(SendDetailForm, self).__init__(*args, **kwargs)
        self.sender=sender
        #self.fields['sender'].intial=sender
        wallet=get_wallet_profile_by_id(self.sender)
        print(f'sender (at constr): {sender}')
        self.fields['currency'].initial=wallet.currency
      
    def clean(self):
        data= super().clean()
        amount=data.get('amount')
        curr=data.get('currency')
        print(f'sender: {self.sender}, amount: {amount}, curr: {curr}')
        if amount and curr and self.sender:
            
            try:
                balance_check(self.sender,Decimal(amount),curr)
                return data
            except TransferException as e:
                print(f'transfer-exception {e}')
                self.add_error('amount',ValidationError(str(e.message)))
            except Exception as e:
                print(f'normal-exception {e}')
                self.add_error('amount',ValidationError(str(e)))
        else:
            self.add_error('currency',ValidationError('Insufficient Parameters'))
        
        

class RequestDetailForm(forms.Form):
       
    amount=forms.DecimalField(decimal_places=2,widget=forms.NumberInput(
        attrs={'placeholder': 'Eg: $200.00',
               'type':'number'
               }), required=True,validators=[],label=None)
    currency=forms.ChoiceField(choices=Currency.choices, widget=forms.Select(
        attrs={'placeholder': 'Select Currency',
               }
    ))
   
    wallet=None
   
    def __init__(self,sender,*args, **kwargs):        
        super(RequestDetailForm, self).__init__(*args, **kwargs)
        self.sender=sender
        wallet=get_wallet_profile_by_id(self.sender)
        self.fields['currency'].initial=wallet.currency

    
      
    # def clean(self):
    #     data= super().clean()
    #     amount=data.get('amount')
    #     curr=data.get('currency')

    #     if amount and curr and self.sender:
    #         try:
    #             balance_check(self.sender,int(amount),curr)
    #             return data
    #         except TransferException as e:
    #             self.add_error('amount',ValidationError(str(e.message)))
    #         except Exception as e:
    #             self.add_error('amount',ValidationError(str(e)))
    #     else:
    #         self.add_error('currency',ValidationError('Insufficient Parameters'))
        
        
            

        

                
class BankAccountForm(forms.Form):
    bank_name=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Name of your Bank'}), required=True,validators=[])
    acc_no=forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Account Number'}), required=True,validators=[])
    
    def save(self, user):
        data=super().clean()
        name=data['bank_name']
        no=data['acc_no']
        try:
            return add_bank_account(name,no,user)
        except Exception as e:
            self.add_error('acc_no',ValidationError(str(e)))

    
