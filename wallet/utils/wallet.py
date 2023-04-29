from account.models import Currency
from ..models import Wallet
from .exceptions.TransactionException import TransferException
import decimal

conversion = {
    'USD': {
        'GBP': 2,
        'EUR': 4,
        'USD': 1.0
    },
    'GBP': {
        'GBP': 1.0,
        'EUR': 5,
        'USD': 0.5
    },
    'EUR': {
        'GBP': 0.5,
        'EUR': 1.0,
        'USD': 0.25
    }
}


def deduct_money_from_wallet(wallet: Wallet, amount: decimal.Decimal, currency):
    currency = currency or wallet.currency
    amount_in_base_currency = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance -= decimal.Decimal(amount_in_base_currency)
    wallet.save()
    return wallet.balance


def add_money_to_wallet(wallet: Wallet, amount: decimal.Decimal, currency):
    currency = currency or wallet.currency
    amount_in_base_currency = amount * decimal.Decimal(conversion[currency][wallet.currency])
    wallet.balance += decimal.Decimal(amount_in_base_currency)
    wallet.save()
    return wallet.balance


def balance_check(sender_id, amount: decimal.Decimal, currency):
    sender_wallet = Wallet.objects.get(user_id=sender_id)
    sender_balance = sender_wallet.balance * decimal.Decimal(conversion[sender_wallet.currency][currency])
    required_balance = amount * decimal.Decimal(conversion[currency][sender_wallet.currency])

    if amount > sender_balance:
        raise TransferException(
            f'Insufficient funds: You require {required_balance} in {sender_wallet.currency} to proceed with this '
            f'transaction.')
    return {
        'balance': sender_balance - required_balance,
        'currency': sender_wallet.currency,
        'success': True
    }


def convert_amount(amount: decimal.Decimal, from_currency: Currency, to_currency: Currency):
    return amount * decimal.Decimal(conversion[from_currency][to_currency])


def change_currency(user_wallet: Wallet, currency: Currency):
    user_wallet.balance = convert_amount(user_wallet.balance, user_wallet.currency, currency)
    user_wallet.currency = currency
    user_wallet.save()
    return True
