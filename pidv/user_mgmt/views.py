from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# This function returns welcome screeen
def homepage(request):
	return render(request=request, 
				  template_name="user_mgmt/homepage.html",
				 )	