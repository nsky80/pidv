from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.sessions.models import Session
from django.utils import timezone
# Create your views here.


# This function returns welcome screeen
def homepage(request):
	return render(request=request, 
				  template_name="user_mgmt/homepage.html",
				 )	


def login_request(request):
    if request.user.is_authenticated:
        # return HttpResponse('<script>history.back();</script>')
        return redirect("account")
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                # return HttpResponse('<script>javascript:history.go(-2);</script>')
                return redirect("/dashboard")
            else:
                messages.error(request, "Invalid username or password!")
        else:
            messages.error(request, "Invalid username or password!")
    form = AuthenticationForm()
    return render(request=request, 
                    template_name="user_mgmt/login.html",
                    context={"form":form}
                    )


def logout_request(request):
	logout(request)
	messages.info(request, "Logged out successfully!")
	return redirect("/")


# For registering new user			 
def register(request):
	if request.user.is_authenticated:
		return redirect("account")
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f"New account created: {username}")
			login(request, user)
			return redirect("/dashboard")
		else:
			for msg in form.error_messages:
				messages.error(request, f"{msg}:{form.error_messages[msg]}")

			return render(request=request,
							template_name="user_mgmt/register.html",
							context={"form": form})
	form = UserCreationForm
	return render(request=request, 
				  template_name="user_mgmt/register.html",
				  context={"form":form}
				 )


def account(request):
	if request.user.is_authenticated:
		user = request.user
		return render(request=request, 
				  template_name="user_mgmt/account.html",
				  context={"user":user},
				 )
	else:
		return redirect("user_mgmt:login")


# This is used for authenticated users
def dashboard(request):
    if request.user.is_authenticated:
        return render(request=request, template_name="user_mgmt/dashboard.html")
    else:
        return redirect("/")