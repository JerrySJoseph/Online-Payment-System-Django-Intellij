from django.contrib.auth.models import User
from django.db.models import Q

def search_with_identifier(identifier):
    result=User.objects.filter(
        Q(email__startswith=identifier)|
        Q(first_name__startswith=identifier)|
        Q(last_name__startswith=identifier) |
        Q(username__startswith=identifier)        
    )
    return list(result.all())

def get_user_with_username(username):
    result=User.objects.get(username=username)
    return result;

def get_user_with_id(id):
    result=User.objects.get(id=id)
    return result;