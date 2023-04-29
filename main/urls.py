from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('logout/', views.logout, name='logout')
]

htmxpatterns = [
    path('htmx/alert', views.alert, name='alert'),
    path('htmx/404', views.page_not_found_404, name='page-not-found-404')
]

urlpatterns += htmxpatterns
