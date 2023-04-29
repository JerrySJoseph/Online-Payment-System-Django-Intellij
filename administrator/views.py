from django.shortcuts import render
from .utils.data import get_no_of_transactions, get_no_of_users, get_all_transactions, get_all_users
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
    users = get_all_users(request.user) or []
    if users is None or len(users) == 0:
        return empty_view(request, 'No users Found',
                          'We did not find any users yet. Whenever a new user registers, this page will show them.')
    context = {
        'users': users,
    }
    return render(request, 'administrator/partials/users_list.html', context)


@admin_required(login_url='login')
def all_transactions(request):
    transactions = get_all_transactions()

    if transactions is None or len(transactions) == 0:
        return empty_view(request, 'No Transactions Found',
                          'We did not find any transactions yet. Whenever a user completes a transaction, this page '
                          'will show them.')
    context = {
        'transactions': transactions,
    }
    return render(request, 'administrator/all-transactions.html', context)


@admin_required(login_url='login')
def index_transactions(request):
    return render(request, 'administrator/all-transactions.html')


@admin_required(login_url='login')
def index_users(request):
    return render(request, 'administrator/all-users.html')


@admin_required(login_url='login')
def add_admin(request):
    form = RegisterForm(is_superuser=True)
    if request.method == 'POST':
        form = RegisterForm(True, request.POST)
        if form.is_valid():
            try:
                user = form.save(is_admin=True)
                return ToastHttpResponse(True, 'Admin User Created', f'You have successfully created an admin account '
                                                                     f'for {user.first_name} {user.last_name}')
            except Exception as e:
                return ToastHttpResponse(False, 'Error Occurred', f'Some error occurred while creating this user. '
                                                                  f'Please try again later {str(e)}')

        else:
            return render(request, 'administrator/partials/add-admin.html', {'form': form})

    return render(request, 'administrator/partials/add-admin.html', {'form': form})
