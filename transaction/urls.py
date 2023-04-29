from django.urls import path
from . import views

urlpatterns=[
       path('',views.index,name='transaction')
]

htmxpatterns=[
    path('htmx/get-transaction-list',views.get_list,name='get-transaction-list'),
    path('htmx/get-transaction-detail',views.get_transaction_detail,name='get-transaction-detail')
]

urlpatterns+=htmxpatterns