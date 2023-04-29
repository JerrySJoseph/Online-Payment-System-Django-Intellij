from django.shortcuts import render
from banking.utils.bank_account import get_all_bank_accounts
from utils.toast import ToastHttpResponse
from .utils.wallet import add_money_to_wallet,change_currency
from decimal import Decimal
from .forms import AddMoneyForm,ChangeCurrencyForm
from utils.views.empty import empty_view
from django.contrib.auth.decorators import login_required


#index page of wallet app
@login_required(login_url='login')
def index(request):
    context = {
        'accounts': get_all_bank_accounts(request.user.id)
    }
    return render(request, 'wallet/layout/index.html', context)

# Http response with AddmoneyForm
@login_required(login_url='login')
def get_add_money(request):

    # handle form submition
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)

        # form validation
        if form.is_valid():
            amount = request.POST.get('amount')
            
            # access local api to add money to wallet
            add_money_to_wallet(request.user.wallet, Decimal(
                amount), request.user.wallet.currency)
            
            # return a success Toast message
            return ToastHttpResponse(True, 'Money Credited', f'{amount} added successfully to your wallet')
        
        # invalid form handle
        else:
            context = {
                'form': form
            }
            return render(request, 'wallet/partials/add_money_amount_form.html', context)
    
    # id tag in GET request denoted user has browsed to this url via user search
    if 'id' in request.GET:
        context = {
            'form': AddMoneyForm()
        }
        return render(request, 'wallet/partials/add_money_amount_form.html', context)
    
    # fetch all available bank accounts of the user
    accounts=get_all_bank_accounts(request.user.id)
    
    # handle no banks accounts listed case with an empty partial page response
    if len(accounts)<=0:
        return empty_view(request,'No Banks added','You have not added any accounts yet.')
    context = {
        'accounts': accounts
    }
    return render(request, 'wallet/partials/add_money_bank_select.html', context)

# Http response with Change Money Form
@login_required(login_url='login')
def get_change_currency(request):
    form=ChangeCurrencyForm(request.user.wallet.currency)

    # handle post request for submitted forms
    if request.method=='POST':
        form=ChangeCurrencyForm(request.user.wallet.currency,request.POST)

        #check if form is valid
        if form.is_valid():
            currency=form.cleaned_data['currency']
            # use local api to change currency
            change_currency(request.user.wallet,currency)
            #return success Toast
            return ToastHttpResponse(True,'Currency Changed',f'You have successfully changed default currency to {currency}')
        # return error toast on invalid form
        return ToastHttpResponse(False,'Error Occured','Some error occured while changing your default currency. Please try again later')
    
    # return new form for new GET requests
    return render(request,'wallet/partials/change_currency.html',{'form':form})


# Http response for Wallet Card
@login_required(login_url='login')
def get_wallet_balance_card(request):
   # return ToastHttpResponse(False)
    return render(request,'wallet/partials/wallet_balance_card.html')

# Http response for Currency Card
@login_required(login_url='login')
def get_currency_card(request):
   # return ToastHttpResponse(False)
    return render(request,'wallet/partials/currency_card.html')