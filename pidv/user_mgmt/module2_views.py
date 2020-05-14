from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from user_mgmt.models import Upload_csv
# import json
import pandas as pd
# import csv
import os
from django.conf import settings
from user_mgmt.module3 import datatable_table_creator
from user_mgmt.forms import RenameColumnForm



# This function used to 
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
                datatable = datatable_table_creator.converter(df)
                # json_data = df.to_json(orient='split')
                # dict_data = df.to_dict('list')
                # return render(request, template_name="module2_html/open_data_file.html", context={"json_data":json_data, "dict_data":dict_data})
                return render(request, template_name="module2_html/open_data_file.html", context={"data_file": datatable})

            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
    raise Http404


# this function usef for downloading of uploaded files
def download_file(request, username, filename):
    if request.user.is_authenticated:
        if "user_" + str(request.user.id) == username:
            try:
                file_path = os.path.join(settings.MEDIA_ROOT, username+'/'+filename)
                if os.path.exists(file_path):
                    with open(file_path, 'rb') as fh:
                        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                        return response
            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
    raise Http404


def delete_data_file(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            # messages.success(request, username)
            try:
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                # instance.delete()
                file_obj.delete()
                messages.success(request, "File Deleted Successfully!")
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))
            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
    raise Http404

# This function handles the preprocessing of Dataset
def preprocess(request, username, filename):
    if request.user.is_authenticated:
        if "user_" + str(request.user.id) == username:
            current_path = "/media/" + username + "/" + filename + "/preprocess"
            current_op = None
            return render(request, template_name='module2_html/preprocess.html', context={"current_url": current_path, "current_op": current_op})
    raise Http404

def renaming(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename + "/preprocess"
                current_op = "renaming"
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                cols_list = list(df.columns)
                if request.method == 'POST':
                    form = RenameColumnForm(cols_list, request.POST or None)
                    if form.is_valid():
                        col1 = form.cleaned_data.get('col1')
                        col2 = form.cleaned_data.get('col2')
                        col3 = form.cleaned_data.get('col3')
                        messages.success(request, [col1, col2, col3])
                        # This will have to change
                        return render(request, template_name="module2_html/preprocess.html", context={"current_url": current_path, "current_op": current_op})
                # messages.success(request, len(cols_list))
                form = RenameColumnForm(cols_list) 
                return render(request=request, template_name='module2_html/renaming.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
    raise Http404


def remove_column(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename + "/preprocess"
                current_op = "remove_column"
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                cols_list = list(df.columns)
                if request.method == 'POST':
                    form = RenameColumnForm(cols_list, request.POST or None)
                    if form.is_valid():
                        col1 = form.cleaned_data.get('col1')
                        col2 = form.cleaned_data.get('col2')
                        col3 = form.cleaned_data.get('col3')
                        messages.success(request, [col1, col2, col3])
                        # This will have to change
                        return render(request, template_name="module2_html/preprocess.html", context={"current_url": current_path, "current_op": current_op})
                # messages.success(request, len(cols_list))
                form = RenameColumnForm(cols_list) 
                return render(request=request, template_name='module2_html/remove_column.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
    raise Http404