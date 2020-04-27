from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseRedirect
from user_mgmt.models import Upload_csv
# from collections import defaultdict
import json
import pandas as pd

def open_data_file(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            # messages.success(request, username)
            try:
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)

                # csv_file = file_obj.uploaded_file
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                data = df.to_json(orient='split')
                return render(request, template_name="module2_html/open_data_file.html", context={"data_file":data})
            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
        else:
            return Http404
    else:
        raise Http404
