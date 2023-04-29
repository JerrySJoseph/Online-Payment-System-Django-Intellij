from django.urls import path
from . import views

urlpatterns=[
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    
]

""" htmxpatterns=[
    path('htmx/iam/login-form',views.get_login_form,name='login-form'),
    path('htmx/iam/register-form',views.get_register_form,name='register-form')
]

urlpatterns+=htmxpatterns """