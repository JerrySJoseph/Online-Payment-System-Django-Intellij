from django.shortcuts import render
from .utils.data import get_no_of_transactions, get_no_of_users, get_all_transactions, get_all_users
from .utils.view_utils import redirect_if_not_super_user
from .decorators import admin_required
from utils.views.empty import empty_view
from iam.forms import RegisterForm
from utils.toast import ToastHttpResponse


@admin_required(login_url='login')
def index(request):
    context = {
        'users': get_no_of_users(),
        'success_transactions': get_no_of_transactions(True),
        'pending_transactions': get_no_of_transactions(False)
    }
    return render(request, 'administrator/dashboard.html', context)


@admin_required(login_url='login')
def all_users(request):
   # redirect_if_not_super_user(request)
    users = get_all_users(request.user) or []
    if users is None or len(users) == 0:
        return empty_view(request, 'No users Found', 'We didnot find any users yet. Whenever a new user registers, this page will show them.')
    context = {
        'users': users,
    }
    return render(request, 'administrator/partials/users_list.html', context)


@admin_required(login_url='login')
def all_transactions(request):
   # redirect_if_not_super_user(request)
    transactions = get_all_transactions()

    if transactions is None or len(transactions) == 0:
        return empty_view(request, 'No Transactions Found', 'We didnot find any transactions yet. Whenever a user completes a transaction, this page will show them.')
    context = {
        'transactions': transactions,
    }
    return render(request, 'administrator/all-transactions.html', context)


@admin_required(login_url='login')
def index_transactions(request):
    # redirect_if_not_super_user(request)
    return render(request, 'administrator/all-transactions.html')


@admin_required(login_url='login')
def index_users(request):
    # redirect_if_not_super_user(request)
    return render(request, 'administrator/all-users.html')


@admin_required(login_url='login')
def add_admin(request):
    # redirect_if_not_super_user(request)
    form = RegisterForm(is_superuser=True)
    if request.method == 'POST':
        form = RegisterForm(True,request.POST)
        if form.is_valid():
            try:
                user = form.save(is_admin=True)
                return ToastHttpResponse(True, 'Admin User Created', f'You have successfully created an admin account for {user.first_name} {user.last_name}')
            except Exception as e:
                return ToastHttpResponse(False, 'Error Occured', f'Some error occured while creating this user. Plese try again later {str(e)}' )
        
        else:
            return render(request, 'administrator/partials/add-admin.html', {'form': form})

    return render(request, 'administrator/partials/add-admin.html', {'form': form})
