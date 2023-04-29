from django.shortcuts import redirect, render
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def alert(request):

    context={
        'success':request.GET.get('success') or False,
        'title':request.GET.get('title') or 'Alert Title',
        'message':request.GET.get('message') or 'This is an alert message'
    }
    return render(request,'main/partials/alert.html',context)

@login_required(login_url='login')
def index(request):
    if request.user.is_superuser:
        return redirect('admin')
    return render(request,'main/dashboard.html',{'title':'Dashboard'})


def logout(request):
    _logout(request)
    return redirect('login')
