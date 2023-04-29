from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from transaction.utils.transactions import get_distinct_transactions_by_id
from utils.toast import ToastHttpResponse
from utils.views.empty import empty_view
from .forms import EditProfileForm


# index page
@login_required(login_url='login')
def index(request):
    return render(request, 'account/index.html')


# GET profile partial html
@login_required(login_url='login')
def get_profile_html(request):
    return render(request, 'account/partials/profile.html')


# GET navbar dropdown partial html for logged in user
@login_required(login_url='login')
def nav_account_details(request):
    return render(request, 'account/partials/nav-account-details.html', {
        'user': request.user
    })


# GET recent transfers table
@login_required(login_url='login')
def get_recent_transfers(request):
    transfers = get_distinct_transactions_by_id(request.user.id)
    if transfers is None or len(transfers) == 0:
        return empty_view(request, 'No Transactions yet',
                          'You have not done any transactions yet. All your recent recipients will show up here.')
    context = {
        'transfers': transfers
    }
    return render(request, 'account/partials/recent-transfer-list.html', context)


# GET edit profile form
@login_required(login_url='login')
def edit_profile(request):
    form = EditProfileForm(request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.user, request.POST)
        if form.is_valid():
            new_user = form.save()
            return ToastHttpResponse(True, 'User Profile Changed', 'Your profile has been successfully changed.')

    context = {
        'form': form,
        'user': request.user
    }
    return render(request, 'account/partials/edit-profile.html', context)

# GET profile card html for logged in user
@login_required(login_url='login')
def profile_card(request):
    return render(request, 'account/partials/profile-card.html')
