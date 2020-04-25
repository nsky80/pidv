from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from .forms import EditProfileForm, ContactForm, FeedbackForm
from django.contrib.auth.models import User		# for community tab purpose
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


# for editing existing user profile
def edit_profile(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			form = EditProfileForm(request.POST, instance=request.user)

			if form.is_valid():
				try:
					form.save()
					return redirect("/account")
				except Exception as ex:
					messages.error(request, f"Please Give Error as Feedback to developers {ex}")
		else:
			form = EditProfileForm(instance=request.user)
			args = {'form': form}
			return render(request=request,
						  template_name="user_mgmt/edit_user_profile.html",
						  context=args)
	else:
		return HttpResponseNotFound()         


def feedback(request):
	if request.method == "POST":
		form = FeedbackForm(request.POST, request.FILES)
		if form.is_valid():
			form.save(commit=True)
			messages.success(request, f"Feedback sent successfully!")
			return redirect("/")
		else:
			messages.error(request, f"Please Write Content!")
			return render(request=request,
							template_name="user_mgmt/feedback.html",
							context={"form": form})
	form = FeedbackForm
	return render(request=request, 
				template_name="user_mgmt/feedback.html",
				context={"form":form}
				)


def community(request):
	if request.user.is_authenticated:
		active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
		user_id_list = []
		for session in active_sessions:
			data = session.get_decoded()
			user_id_list.append(data.get('_auth_user_id', None))
		# Query all logged in users based on id list
		users =  User.objects.filter(id__in=user_id_list)
		return render(request=request, 
					template_name="user_mgmt/community.html",
					context={"users": users},
					)
	else:
		messages.warning(request, f"For Community Login first!")
		return redirect("/login")
				 

def help(request):
	return render(request=request, template_name="user_mgmt/under_construction.html")


def under_construction(request, slug):
	messages.success(request, slug)
	messages.error(request, "Either this page is under construction or invalid url!")
	return render(request=request, template_name="user_mgmt/under_construction.html")
