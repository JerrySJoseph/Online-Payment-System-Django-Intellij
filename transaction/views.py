from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import Http404
from .utils.transactions import get_transactions_by_id, get_transaction_by_id,get_all_transactions

# Create your views here.

@login_required(login_url='login')
def index(request):
    if request.method == 'GET':
        return render(request, 'transaction/layout/list.html')
    raise Http404()

@login_required(login_url='login')
def get_list(request):
    if request.method == 'GET':
        limit = int(request.GET.get('limit')
                    ) if request.GET.get('limit') else 100
        sort = request.GET.get('sort')
        sortby = request.GET.get('sortby')

        type=request.GET.get('type') or 'user'
        transactions=[]

        if type == 'all':
            transactions=get_all_transactions()
        else:
            transactions = get_transactions_by_id(
                request.user.id, limit=limit, sort=sort, sortby=sortby)
        

        if len(transactions) == 0:
            context = {
                'title': 'No Transactions',
                'message': 'You have not done any transactions yet. Come back here after any transaction to see details.'
            }
            return render(request, 'transaction/partials/empty.html', context)
        
        for tr in transactions:
            if tr.sender.id==request.user.id:
                tr.type='DEBIT'
            else:
                tr.type='CREDIT'
        context = {
            'transactions': transactions,
            'type':type
        }
        return render(request, 'transaction/partials/transaction-table.html', context)
    raise Http404()

@login_required(login_url='login')
def get_transaction_detail(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        transaction = get_transaction_by_id(tid)
        if transaction.sender.id==request.user.id:
            transaction.type='DEBIT'
        else:
            transaction.type='CREDIT'
        context = {
            't': transaction,
        }
        return render(request, 'transaction/partials/transaction-detail.html', context)
    raise Http404()
