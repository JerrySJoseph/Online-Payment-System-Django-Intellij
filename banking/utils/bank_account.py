from ..models import BankAccount
from django.contrib.auth.models import User

#Create a new bank account for User
def add_bank_account(bank_name:str,acc_no:str,user:User)->BankAccount:
    account=BankAccount(bank_name=bank_name,acc_no=acc_no,owner=user)
    account.save()
    return account

#Remove an existing bank account from Database
def remove_bank_account(bank_id:int):
    account=BankAccount.objects.get(id=bank_id)
    account.delete()
    return True

#Edit/Update an existing bank account 
def edit_bank_account(bank_id:int,bank_name:str,acc_no:str,user:User)->BankAccount:
     account=BankAccount.objects.get(id=bank_id)
     account.bank_name=bank_name
     account.acc_no=acc_no
     account.owner=user
     account.save()
     return BankAccount

#Get a list of bank acocunt for an user
def get_all_bank_accounts(user_id:int):
    return BankAccount.objects.filter(owner_id__exact=user_id).all()

def get_bank_account_with_id(id:int):
    return BankAccount.objects.get(id=id)