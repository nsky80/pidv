from django.urls import path
from . import views

app_name = "user_mgmt"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('login', views.login_request, name="login_request"),
    path('logout', views.logout_request, name="logout_request"), 
    path('register', views.register, name="register"),
    path('account', views.account, name="account"), 
    # path('account/edit_profile', views.edit_profile, name="edit_profile"),
    path('help', views.help, name="help"),
    path('feedback', views.feedback, name="feedback"),
    path('<slug>', views.under_construction, name="under_construction"),
]
