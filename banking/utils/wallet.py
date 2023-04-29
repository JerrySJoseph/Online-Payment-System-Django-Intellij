from wallet.models import Wallet

def get_wallet_profile_by_id(userid):
    wallet=Wallet.objects.get(user_id=userid)
    return wallet