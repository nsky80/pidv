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
from user_mgmt.forms import RenameColumnForm, RemoveColumnForm, ColumnForSorting



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
            current_path = "/media/" + username + "/" + filename 
            current_op = "preprocess"
            return render(request, template_name='module2_html/preprocess.html', context={"current_url": current_path, "current_op": current_op})
    raise Http404

def renaming(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename 
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
                        columns_options = [] # this list contain the response of each column
                        # appending data for each response
                        flag = False   # it remains false if no column selected for deletion
                        for i in range(1, 9):    # currently we are supporting 8 columns only
                            ch = form.cleaned_data.get('col%s'%i)
                            # checking whether it is empty or not
                            if ch:
                                columns_options.append(cols_list[i - 1])  # appending the name of given column to be deleted
                                flag = True
                        if flag:
                            messages.success(request, ", ".join(columns_options) + " renamed successfully!")
                        else:
                            messages.info(request, "No changes made!")
                        # This will have to change
                        return redirect("user_mgmt:renaming", username=username, filename=filename)
                        # messages.success(request, len(cols_list))
                form = RenameColumnForm(cols_list) 
                return render(request=request, template_name='module2_html/renaming.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404


def remove_column(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename
                current_op = "remove_column"
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                cols_list = list(df.columns)
                if request.method == 'POST':
                    form = RemoveColumnForm(cols_list, request.POST or None)
                    if form.is_valid():
                        columns_options = [] # this list contain the response of each column
                        # appending data for each response
                        flag = False   # it remains false if no column selected for deletion
                        for i in range(1, 9):    # currently we are supporting 8 columns only
                            ch = form.cleaned_data.get('col%s'%i)
                            # checking whether it is empty or not
                            if ch:
                                columns_options.append(cols_list[i - 1])  # appending the name of given column to be deleted
                                flag = True
                        if flag:
                            messages.success(request, ", ".join(columns_options) + " deleted successfully!")
                        else:
                            messages.info(request, "No changes made!")
                        # This will have to change
                        return redirect("user_mgmt:remove_column", username=username, filename=filename)
                        # return render(request, template_name="module2_html/remove_column.html", context={'form': form, "current_url": current_path, "current_op": current_op})
                form = RemoveColumnForm(cols_list) 
                return render(request=request, template_name='module2_html/remove_column.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404


def sorting(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename 
                current_op = "sorting"
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                cols_list = [('0', 'Select Column')]
                for i, col_name in enumerate((df.columns), 1):
                    cols_list.append((str(i), col_name))

                if request.method == 'POST':
                    form = ColumnForSorting(cols_list, request.POST or None)
                    if form.is_valid():
                        flag = form.cleaned_data.get("col1")
                        if flag == '0':
                            messages.info(request, "No changes made!")
                        else:
                            column_name = cols_list[int(flag)][1]
                            messages.success(request, "Data sorted Successfully w.r.t. " + column_name)
                        # This will have to change
                        return redirect("user_mgmt:sorting", username=username, filename=filename)
                form = ColumnForSorting(cols_list) 
                return render(request=request, template_name='module2_html/sorting.html', context= {'form':form, "current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404



def cleaning(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename 
                current_op = "cleaning"
                return render(request=request, template_name='module2_html/cleaning.html', context= {"current_url": current_path, "current_op": current_op})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404


def under_construction(request, username, filename, slug="Coming Soon"):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename 
                current_op = "preprocess"
                messages.info(request, str(slug) + " feature coming soon..")
                return render(request=request, template_name='module2_html/under_construction.html', context= {"current_url": current_path, "current_op": current_op})

