from wallet.models import Wallet
from wallet.utils.wallet import balance_check,deduct_money_from_wallet,add_money_to_wallet
from transaction.models import TransactionType, TransactionStatus
from django.contrib.auth.models import User
from transaction.utils.transactions import create_transaction,_generate_transaction_id
from ..models import TransferRequest
from django.db.models import Q
from notification.utils.notifications import notify_user,NotificationType
import decimal



def transfer_money_by_id(sender_id, recipient_id, amount, currency):
    if not type(amount)=='Decimal':
        amount=decimal.Decimal(amount)
    balance_check(sender_id,amount,currency)
    #raise TransferException('Some random transfer exception')
    return _transfer_money_by_id(sender_id,recipient_id,amount,currency)

def _transfer_money_by_id(sender_id, recipient_id, amount, currency,notify:bool=True):

    sender=User.objects.get(id=sender_id)
    recipient=User.objects.get(id=recipient_id)

    # deduct money from sender wallet
    sender_wallet = Wallet.objects.get(user_id=sender.id)
    sender_balance=deduct_money_from_wallet(sender_wallet, amount, currency)

    # add money to recipient wallet
    recipient_wallet = Wallet.objects.get(user_id=recipient.id)
    recipient_balance=add_money_to_wallet(recipient_wallet, amount, currency)

    tid=_generate_transaction_id()
    
    # create sender debit transaction
    create_transaction(tid,sender,recipient,TransactionStatus.SUCCESS,amount,currency,sender_balance)
    
    # # create recipient credit transaction
    # create_transaction(tid,recipient,sender,recipient,TransactionType.CREDIT,TransactionStatus.SUCCESS,amount,currency,recipient_balance)
    
    if notify:
        notify_user(sender_id,'Money Transferred',f'You have transferred {amount} {currency} to {recipient.first_name} {recipient.last_name}',type=NotificationType.TRANSACTION_SUCCESS)
        notify_user(recipient_id,'Money Recieved',f'You have recieved {amount} {currency} from {sender.first_name} {sender.last_name}',type=NotificationType.MONEY_RECIEVED)
    return True

def create_transfer_request(sender_id:int, recipient_id:int,amount,currency):
    rid=_generate_transaction_id()
    sender=User.objects.get(id=sender_id)
    recipient=User.objects.get(id=recipient_id)
    tr_request=TransferRequest(
        rid=rid,
        sender=sender,
        recipient=recipient,
        source=sender,
        amount=decimal.Decimal(amount),
        currency=currency,
    )
    tr_request.save()
    notify_user(sender_id,'Transfer Request Sent',f'You have requested {recipient.first_name} an amount of {amount} {currency}.',type=NotificationType.MONEY_REQUEST)
    notify_user(recipient_id,'Transfer Request Recieved',f'{recipient.first_name} has requested an amount of {amount} {currency}.',type=NotificationType.MONEY_REQUEST)

def get_transfer_requests_by_id_qs(user_id:int)->list:
    return list(get_transfer_requests_by_id(user_id))

def get_transfer_requests_by_id(user_id:int,group='all')->list:
    
    if group=='sent':
        query=Q(sender_id__exact=user_id)
    elif group=='recieved':
        query=Q(recipient_id__exact=user_id)
    else :
        query=Q(sender_id__exact=user_id)|Q(recipient_id__exact=user_id)
    transactions=TransferRequest.objects.filter(
        query
    )
    return transactions.all()

def get_transfer_request_by_id(rid:int):
    return TransferRequest.objects.get(id=rid)

def withdraw_transfer_request(rid:int):
    request=get_transfer_request_by_id(rid)
    request.delete()
    
    return True

def approve_transfer_request(rid:int):
    request=get_transfer_request_by_id(rid)
    transfer_money_by_id(sender_id=request.recipient.id,recipient_id=request.sender.id,amount=request.amount,currency=request.currency)
    request.delete()
    return True

def deny_transfer_request(rid:int):
    request=get_transfer_request_by_id(rid)
    request.delete()
    return True