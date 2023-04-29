from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification
from .utils.notifications import get_notifications_for_user

@login_required(login_url='login')
def get_notifications_panel(request):
    notifications=get_notifications_for_user(request.user.id,limit=5)
    context={
        'notifications':notifications.all(),
        'count':len(notifications)
    }
    return render(request,'notification/layout/notification-list.html',context)