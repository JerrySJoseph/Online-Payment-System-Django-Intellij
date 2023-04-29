from .forms import BankAccountForm
from django.shortcuts import render,HttpResponse
from .utils.bank_account import get_all_bank_accounts,remove_bank_account,get_bank_account_with_id
from utils.toast import ToastHttpResponse
from utils.views import empty

def get_add_bank_account_form(request):
    
    form=BankAccountForm()
    
    if request.method=='POST':
        form=BankAccountForm(request.POST)
        if form.is_valid():
            account=form.save(request.user)
            return ToastHttpResponse(success=True,title='New Bank account added',message=f'{account.bank_name} has been added to your account.')
    return render(request,'banking/partials/bank_account_add.html',{'form':form})


def get_bank_account_list(request):
    if not request.method=='GET':
        return ToastHttpResponse(success=False,title='Error occured',message='Not Allowed')
    user_id=request.GET.get('user_id')
    if not user_id:
        return ToastHttpResponse(success=False,title='Error occured',message='Not Allowed')
    
    accounts=get_all_bank_accounts(user_id)
    if len(accounts)<=0:
        return empty.empty_view(request,'No Banks added','You have not added any accounts yet.')
    
    context={
        'accounts':accounts
    }
    return render(request,'banking/partials/bank_account_list.html',context)

def delete_bank_account(request):
    
    if request.method=='POST':
        id=request.POST.get('id')
        remove_bank_account(id)
        return ToastHttpResponse(success=True,title='Bank account removed',message='Bank account has been successfully removed from your account')
    context={
        'account':get_bank_account_with_id(id=request.GET.get('id'))
    }
    return render(request,'banking/partials/bank_account_delete_confirmation.html',context)