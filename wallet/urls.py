from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='wallet')
]

htmxpatterns=[
    path('htmx/add-money',views.get_add_money,name='add-money'),
    path('htmx/change-currency',views.get_change_currency,name='change-currency'),
    path('htmx/wallet-balance-card',views.get_wallet_balance_card,name='wallet-balance-card'),
    path('htmx/currency-card',views.get_currency_card,name='currency-card')
]

urlpatterns+=htmxpatterns