from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login as _login, authenticate
from iam.forms import RegisterForm, LoginForm
from django.contrib.messages import info, error, get_messages
from utils.toast import ToastHttpResponse
from django.contrib.auth.models import User

def register(request):
    create_default_superuser()
    if request.method == 'POST':
        form = RegisterForm(False,request.POST)
        print('----POST---')
        if form.is_valid():
            print('----form is valid---')
            form.save()
            return redirect('login')
        else:
            return render(request, 'iam/register.html', {'title': 'Create account', 'form': form})
    else:
        return render(request, 'iam/register.html', {'title': 'Create account', 'form': RegisterForm()})


def login(request):
    create_default_superuser()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                _login(request, user)
                return HttpResponseRedirect('/')
            else:
                error(request, 'Invalid username or password')

        else:
            error(request, 'Invalid username or password')
            message_store = get_messages(request)
            context = {'title': 'Sign In',
               'form': form, 'messages': message_store}
            return render(request, 'iam/login.html', context)
    form = LoginForm()
    message_store = get_messages(request)
    context = {'title': 'Sign In',
               'form': form, 'messages': message_store}
    message_store.used = True
    return render(request, 'iam/login.html', context)

def create_default_superuser():
    if not User.objects.filter(username='admin1').exists():
        User.objects.create_superuser(username='admin1',password='admin1')