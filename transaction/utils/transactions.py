from ..models import Transaction
from django.db.models import Q
from django.contrib.auth.models import User
from transaction.models import TransactionType, TransactionStatus
import uuid


def get_transactions_by_id_qs(user_id:int):
    return get_transactions_by_id(user_id)

def get_transactions_by_id(user_id:int,limit=100,sort='dsc',sortby='datetime')->list:
    transactions=Transaction.objects.filter(
        Q(sender_id__exact=user_id)|
        Q(recipient_id__exact=user_id)
    )
    
    sortby=sortby or 'datetime'
    if sort =='asc':
        orderby=sortby
    else:
        orderby=f'-{sortby}'
    return transactions.all().order_by(orderby)[:limit]

def get_distinct_transactions_by_id(user_id:int):
    transactions=Transaction.objects.filter(
        Q(sender_id__exact=user_id)|
        Q(recipient_id__exact=user_id)
    )
    a=[]
    
   
    for tran in transactions:
        if not tran.recipient in a:
            a.append(tran.recipient)
    return a

def create_transaction(transaction_id:str,sender: User, recipient: User, status: TransactionStatus, amount, currency,balance):
    
    transaction=Transaction(
        tid=transaction_id,
        sender=sender,
        recipient=recipient,
        amount=amount,
        currency=currency,
        status=status,
        balance=balance
    )
    transaction.save()


def get_transaction_by_id(id:int):
    return Transaction.objects.get(id=id)

def _generate_transaction_id():
    return uuid.uuid4()

def get_all_transactions():
    return Transaction.objects.all()