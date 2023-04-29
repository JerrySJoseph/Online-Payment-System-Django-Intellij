import json

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, HttpResponse
from utils.toast import ToastHttpResponse
from wallet.utils.exceptions.TransactionException import TransferException
from .forms import SearchForm, SendDetailForm, RequestDetailForm
from .utils.search import get_user_with_id
from .utils.transfers import create_transfer_request, transfer_money_by_id, get_transfer_requests_by_id, \
    get_transfer_request_by_id, withdraw_transfer_request, approve_transfer_request as atr, deny_transfer_request as dtr


@login_required(login_url='login')
def transfer_request(request):
    if request.method == 'GET':
        return render(request, 'banking/layout/transfer-request.html')
    raise Http404()


@login_required(login_url='login')
def get_transfer_request_list(request):
    if request.method == 'GET':
        group = request.GET.get('group') if request.GET.get(
            'group') is not None else 'all'
        results = []

        results = get_transfer_requests_by_id(request.user.id, group)
        context = {
            'transfer_requests': results,
            'group': group,
            'count': len(results)
        }
        print(len(results))
        return render(request, 'banking/partials/transfer_request_list.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def withdraw_confirmation_form(request):
    if request.method == 'GET':
        context = {
            'rid': request.GET.get('rid')
        }
        return render(request, 'banking/partials/transfer_request_withdraw.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def approve_tr_confirmation_form(request):
    if request.method == 'GET':
        context = {
            'tr': get_transfer_request_by_id(request.GET.get('rid'))
        }
        return render(request, 'banking/partials/transfer_request_approve.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def deny_tr_confirmation_form(request):
    if request.method == 'GET':
        context = {
            'tr': get_transfer_request_by_id(request.GET.get('rid'))
        }
        return render(request, 'banking/partials/transfer_request_deny.html', context)
    return HttpResponse('No content')


@login_required(login_url='login')
def withdraw_request(request):
    if request.method == 'GET':
        rid = request.GET.get('rid')
        tr_rq = get_transfer_request_by_id(rid)
        withdraw_transfer_request(rid)
        return ToastHttpResponse(True, 'Request Withdrawn',
                                 f'Transfer request of {tr_rq.currency} {tr_rq.amount} was withdrawn successfully')

    return HttpResponse('No content')


@login_required(login_url='login')
def approve_transfer_request(request):
    if request.method == 'GET':
        try:

            rid = request.GET.get('rid')
            tr_rq = get_transfer_request_by_id(rid)
            atr(rid)
            return ToastHttpResponse(True, 'Money Transferred',
                                     f'You have sent {tr_rq.recipient.first_name} an amount of {tr_rq.currency} {tr_rq.amount} successfully')
        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'banking/partials/send_failed.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed:{str(e)}')

    return HttpResponse('No content')


@login_required(login_url='login')
def deny_transfer_request(request):
    if request.method == 'GET':
        try:

            rid = request.GET.get('rid')
            tr_rq = get_transfer_request_by_id(rid)
            dtr(rid)
            return ToastHttpResponse(True, 'Transfer Request Declined',
                                     f'You have declined the transfer request from {tr_rq.recipient.first_name} for an amount of {tr_rq.currency} {tr_rq.amount} successfully')

        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'banking/partials/send_failed.html', context)
        except Exception as e:
            return ToastHttpResponse(False, 'Error Occured', f'{str(e)}')

    return HttpResponse('No content')


@login_required(login_url='login')
def send(request):
    form = SearchForm()
    results = []
    # after confirmation
    if request.method == 'GET':
        if 'identifier' in request.GET:
            form = SearchForm(request.GET)

        if form.is_valid():
            results = form.search()

        return render(request, 'banking/layout/send.html', {'form': form, 'search_results': results})
    else:
        raise Http404()


@login_required(login_url='login')
def send_detail_form(request):
    print(f'user:{request.user}')
    if request.method == 'POST' and not 'confirm' in request.POST:
        recipient = get_user_with_id(request.POST.get('recipient'))
        form = SendDetailForm(request.user.id, request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'recipient': recipient,
                'sender': request.user,
                'amount': request.POST.get('amount'),
                'currency': request.POST.get('currency')
            }
            return render(request, 'banking/partials/send_confirm_form.html', context)
        context = {
            'form': form,
            'recipient': recipient
        }
        return render(request, 'banking/partials/send_detail_form.html', context)

    elif request.method == 'POST' and 'confirm' in request.POST:

        try:
            sender_id = request.POST.get('sender')
            recipient_id = request.POST.get('recipient')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            recipient = get_user_with_id(recipient_id)
            transfer_money_by_id(sender_id, recipient_id, amount, currency)
            return HttpResponse(status=204, headers={
                'HX-Trigger': json.dumps({
                    'toast': {
                        'success': True,
                        'title': 'Money Transferred',
                        'message': f'You have successfully transfered {amount} {currency} to {recipient.first_name}.'
                    }
                })
            })

        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'banking/partials/send_failed.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed:{str(e)}')

    elif 'recipient' not in request.GET:
        raise Http404()
    recipient = get_user_with_id(request.GET.get('recipient'))
    context = {
        'form': SendDetailForm(request.user.id),
        'recipient': recipient
    }
    return render(request, 'banking/partials/send_detail_form.html', context)


@login_required(login_url='login')
def detail_form(request):
    if 'type' in request.GET:
        if request.GET.get('type') == 'request':
            return request_detail_form(request)
        if request.GET.get('type') == 'send':
            return send_detail_form(request)
    raise Http404()


@login_required(login_url='login')
def request(request):
    form = SearchForm()
    results = []
    # after confirmation
    if request.method == 'GET':
        if 'identifier' in request.GET:
            form = SearchForm(request.GET)

        if form.is_valid():
            results = form.search()

        return render(request, 'banking/layout/request.html', {'form': form, 'search_results': results})
    else:
        raise Http404()


@login_required(login_url='login')
def request_detail_form(request):
    print(f'user:{request.user}')
    if request.method == 'POST' and not 'confirm' in request.POST:
        recipient = get_user_with_id(request.POST.get('recipient'))
        form = RequestDetailForm(request.user.id, request.POST)
        if form.is_valid():
            context = {
                'form': form,
                'recipient': recipient,
                'sender': request.user,
                'amount': request.POST.get('amount'),
                'currency': request.POST.get('currency')
            }
            return render(request, 'banking/partials/request_confirm_form.html', context)
        context = {
            'form': form,
            'recipient': recipient
        }
        return render(request, 'banking/partials/request_detail_form.html', context)

    elif request.method == 'POST' and 'confirm' in request.POST:

        try:
            sender_id = request.POST.get('sender')
            recipient_id = request.POST.get('recipient')
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            create_transfer_request(sender_id, recipient_id, amount, currency)
            context = {
                'form': RequestDetailForm(request.user.id, request.POST),
                'recipient': get_user_with_id(recipient_id),
                'sender': request.user,
                'amount': amount,
                'currency': currency
            }
            return render(request, 'banking/partials/request_success.html', context)
        except TransferException as te:
            context = {
                'message': te.message
            }
            return render(request, 'banking/partials/request_failed.html', context)
        except Exception as e:
            return HttpResponse(f'Transaction Failed:{str(e)}')

    elif 'recipient' not in request.GET:
        raise Http404()
    recipient = get_user_with_id(request.GET.get('recipient'))
    context = {
        'form': RequestDetailForm(request.user.id),
        'recipient': recipient
    }
    return render(request, 'banking/partials/request_detail_form.html', context)


@login_required(login_url='login')
def bank_accounts(request):
    return render(request, 'banking/layout/bank-accounts.html')
