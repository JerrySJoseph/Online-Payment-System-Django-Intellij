from django.urls import path
from . import views
from .bank_account_views import get_add_bank_account_form, get_bank_account_list,delete_bank_account
from .apis import transfers as transfer_apis

urlpatterns = [
    path('send/', views.send, name='send-money'),
    path('request/', views.request, name='request-money'),
    path('transfer-request/', views.transfer_request, name='transfer-request'),
    path('bank-accounts/', views.bank_accounts, name='bank-accounts'),
]

htmxpatters = [
    path('htmx/detail-form', views.detail_form, name='detail-form'),
    path('htmx/send-detail-form', views.send_detail_form, name='send-detail-form'),
    path('htmx/request-detail-form', views.request_detail_form,
         name='request-detail-form'),
    path('htmx/transfer-request-list',
         views.get_transfer_request_list, name='transfer-request-list'),
    path('htmx/withdraw-transfer-request-form',
         views.withdraw_confirmation_form, name='withdraw-form'),
    path('htmx/approve-transfer-request-form',
         views.approve_tr_confirmation_form, name='transfer-request-approve-confirmation'),
    path('htmx/deny-transfer-request-form',
         views.deny_tr_confirmation_form, name='transfer-request-deny-confirmation'),
    path('htmx/withdraw-transfer-request',
         views.withdraw_request, name='withdraw-request'),
    path('htmx/deny-transfer-request',
         views.deny_transfer_request, name='deny-request'),
    path('htmx/approve-transfer-request',
         views.approve_transfer_request, name='approve-request'),

    # bank accouunt
    path('htmx/add-bank-account',
         get_add_bank_account_form, name='add-bank-account'),
    path('htmx/delete-bank-account',
         delete_bank_account, name='delete-bank-account'),
    path('htmx/get-bank-account-list',
         get_bank_account_list, name='get-bank-account-list'),

]

urlpatterns += htmxpatters
