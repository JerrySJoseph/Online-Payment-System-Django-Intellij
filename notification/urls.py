from django.urls import path
from . import views

urlpatterns=[
  
]

htmxpatterns=[
    path('htmx/get-notification',views.get_notifications_panel,name='get-notifications')
]
urlpatterns+=htmxpatterns