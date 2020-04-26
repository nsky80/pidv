from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from .forms import EditProfileForm, ContactForm, FeedbackForm, Upload_csvForm
from django.contrib.auth.models import User		# for community tab purpose
from .models import Upload_csv
# from collections import defaultdict
# import json
# import pandas as pd

# Create your views here.


# This function returns welcome screeen
def homepage(request):
	return render(request=request, 
				  template_name="user_mgmt/homepage.html",
				 )	


def login_request(request):
    if request.user.is_authenticated:
        # return HttpResponse('<script>history.back();</script>')
        return redirect("user_mgmt:account")
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
                return redirect("user_mgmt:dashboard")
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
		return redirect("user_mgmt:account")
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


# this shows the information of user
def account(request):
	if request.user.is_authenticated:
		user = request.user
		return render(request=request, 
				  template_name="user_mgmt/account.html",
				  context={"user":user},
				 )
	else:
		return redirect("user_mgmt:login_request")


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


# currently it shows only list of active users
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
				 
 
 # This handles uploading of file

def upload_csv_file(request): 
	if request.user.is_authenticated:
		form = Upload_csvForm(request.POST or None, request.FILES or None) 
		if request.method =='POST': 
			
			if form.is_valid(): 
				
				obj = form.save(commit = False) 
				obj.user = request.user
				obj.save() 
				form = Upload_csvForm() 
				messages.success(request, "File Successfully uploaded!") 
				return redirect("/dashboard")

		return render(request, 'user_mgmt/upload_csv.html', {'form':form}) 
	else:
		messages.error(request, "Login of Signup First!")
		return redirect("user_mgmt:login_request")


# This is used for authenticated users
def dashboard(request):
	if request.user.is_authenticated:
		# files = Upload_csv.objects.filter(request.user == Upload_csv.user) 
		files = Upload_csv.objects.filter(user=request.user)
		return render(request=request, template_name="user_mgmt/dashboard.html", context={"files": files})
	else:
		return redirect("/")


def help(request):
	return render(request=request, template_name="user_mgmt/under_construction.html")


def contribute(request):
	return render(request=request, template_name="user_mgmt/contribute.html")


def open_csv(request, username, filename):
	if request.user.is_authenticated:
		if "user_" + str(request.user.id) == username:
			# messages.error(request, str(request.user.id) + " " + str(username))
			messages.success(request, request.get_full_path())
			return render(request=request, template_name="user_mgmt/experiment.html")

			# try:
			# 	csv_file = request.FILES[request.get_full_path()]
			# 	if not csv_file.name.endswith('.csv'):
			# 		messages.error(request,'File is not CSV type')
			# 		# return HttpResponseRedirect(reverse("open_csv:upload_csv"))
			# 		return redirect("user_mgmt:dashboard")
			# 	#if file is too large, return
			# 	if csv_file.multiple_chunks():
			# 		messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
			# 		return HttpResponseRedirect(reverse("user_mgmt:dashboard"))
			# 	df = pd.read_csv(csv_file)
			# 	messages.success(request, type(df))
			# 	data = df.to_json(orient='split')
			# 	return render(request, template_name="user_mgmt/experiment.html", context={"csv_data": data})

			# except Exception as e:
			# 	# logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
			# 	# messages.error(request,"Unable to upload file. "+repr(e))
			# 	messages.error(request,"Unable to upload file. " + repr(e))

			
			# return HttpResponseRedirect(reverse("user_mgmt:dashboard"))


# template for error handling 
def under_construction(request, slug):
	messages.success(request, slug)
	messages.error(request, "Either this page is under construction or invalid url!")
	return render(request=request, template_name="user_mgmt/under_construction.html")
