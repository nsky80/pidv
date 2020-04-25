from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('login', views.login_request, name="login_request"),
    path('logout', views.logout_request, name="logout_request"), 
    path('register', views.register, name="register"),
    path('account', views.account, name="account"), 
]
