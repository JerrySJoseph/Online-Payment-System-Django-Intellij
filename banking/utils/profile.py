from account.models import Profile

def get_user_profile_by_id(userid):
    user=Profile.objects.get(user_id=userid)
    return user