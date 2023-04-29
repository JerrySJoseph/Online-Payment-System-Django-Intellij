from ..models import NotificationType,Notification
from django.contrib.auth.models import User
from django.db.models import Q
import uuid

def notify_user(userid:int,title:str,message:str,type:NotificationType=NotificationType.INFO):
    notification=Notification(nid=uuid.uuid4(),user=User.objects.get(id=userid),type=type,message=message,title=title)
    notification.save()
    return True


def get_notifications_for_user(userid:int,limit=100):
    limit=limit or 100
    notifications=Notification.objects.filter(
        Q(user_id__exact=userid)
    ).order_by('-datetime')[:limit]
    
    return notifications.all()