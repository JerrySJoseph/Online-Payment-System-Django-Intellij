from django.db import models
from django.contrib.auth.models import User
from account.models import Currency

# Wallet model to access properties related to user wallet
# All the transactions and conversions are processed through user wallets
# Properties:
    # balance: amount of money user has left in panda account
    # currency: Current base currency of users wallet
    # user: The user the wallet corresponds to
class Wallet(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='wallet')
    balance=models.DecimalField(default=1000,decimal_places=2,max_digits=10)
    currency=models.CharField(max_length=5,choices=Currency.choices,default=Currency.USD)

    def __str__(self) -> str:
        return self.user.username