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
from django.core.files.base import ContentFile
from user_mgmt.module2 import general_tool
from django.utils import timezone


# This function used to 
def open_data_file(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            # messages.success(request, username)
            try:
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                df = general_tool.read_dataframe(file_obj)
                datatable = datatable_table_creator.converter(df, 1)   # here 1 indicate that default screen table
                # Prepairing stats 
                perc =[.20, .25, .40, .50, .60, .75, .80] 
                df = df.describe(percentiles = perc, include = 'all') 
                df.insert(loc=0, column="Definition", value=list(df.index))
                stats = datatable_table_creator.converter(df, 3)  # it contains statistics of data
                return render(request, template_name="module2_html/open_data_file.html", context={"data_file": datatable, "stats": stats, "file_obj": file_obj})
            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
    raise Http404


# this function usef for downloading of uploaded files
def download_file(request, username, filename, version):
    if request.user.is_authenticated:
        if "user_" + str(request.user.id) == username:
            try:
                if version == 1:
                    file_path = os.path.join(settings.MEDIA_ROOT, username+'/'+filename)
                elif version == 2:
                    file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                    # checking whether backup created until or not
                    if file_obj.uploaded_file_backup:
                        file_path = os.path.join(settings.MEDIA_ROOT, file_obj.uploaded_file_backup.path)
                    else:
                        raise Exception("This file doesn't modified yet!")
                else:
                    raise Http404
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
                file_obj.uploaded_file.delete()
                file_obj.uploaded_file_backup.delete(save=True)
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

# This renames the column of csv file not other
def renaming(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename 
                current_op = "renaming"
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                # Here we are reading dataframe from another function for security purpose
                df = general_tool.read_dataframe(file_obj)
                cols_list = list(df.columns)
                if request.method == 'POST':
                    form = RenameColumnForm(cols_list, request.POST or None)
                    if form.is_valid():
                        columns_options = [] # this list contain the response of each column
                        # appending data for each response
                        flag = False   # it remains false if no column selected for deletion
                        for i in range(1, min(9, len(cols_list)+1)):    # currently we are supporting 8 columns only
                            ch = form.cleaned_data.get('col%s'%i)
                            # checking whether it is empty or not
                            if ch:
                                columns_options.append(ch)  # appending the name of given column to be deleted
                                flag = True
                            else:
                                columns_options.append(cols_list[i - 1])
                        if flag:
                            # reflecting changes into DataFrame
                            df.columns = columns_options
                            f1 = ContentFile(df.to_csv(index=False))
                            file_obj.last_modified = timezone.now()
                            file_obj.uploaded_file.delete()
                            # trying to flag the old file but incase of renaming we do not need a backup
                            # general_tool.file_backup(file_obj, "renaming", username, filename)
                            file_obj.uploaded_file.save(filename, f1, save=True)
                            # print(type(f1))
                            messages.success(request, "Column(s) Renamed Successfully!")
                            return redirect("user_mgmt:renaming", username=username, filename=filename)
                        else:
                            messages.info(request, "No changes made!")
                        # this return to changed name template
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
                # Here we are reading dataframe from another function for security purpose
                df = general_tool.read_dataframe(file_obj)
                cols_list = list(df.columns)
                if request.method == 'POST':
                    form = RemoveColumnForm(cols_list, request.POST or None)
                    if form.is_valid():
                        columns_options = [] # this list contain the response of each column
                        # appending data for each response
                        flag = False   # it remains false if no column selected for deletion
                        for i in range(1, min(9, len(cols_list)+1)):    # currently we are supporting 8 columns only
                            ch = form.cleaned_data.get('col%s'%i)
                            # checking whether it is empty or not
                            if ch:
                                columns_options.append(cols_list[i - 1])  # appending the name of given column to be deleted
                                flag = True
                        if flag:
                            # deleting the selected column
                            df.drop(columns_options, axis = 1, inplace = True) 

                            f1 = ContentFile(df.to_csv(index=False))
                            # trying to backing up the old file but incase of renaming we do not need a backup
                            general_tool.file_backup(file_obj, "remove_column", username, filename)
                            file_obj.uploaded_file.save(filename, f1, save=True)
                            messages.success(request, ", ".join(columns_options) + " deleted successfully!")
                            return redirect("user_mgmt:remove_column", username=username, filename=filename)

                        else:
                            messages.info(request, "No changes made!")
                            return redirect("user_mgmt:remove_column", username=username, filename=filename)

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
                # prepairing the pandas dataframe
                df = general_tool.read_dataframe(file_obj)
                cols_list = [('0', 'Select Column')]
                for i, col_name in enumerate((df.columns), 1):
                    cols_list.append((str(i), col_name))

                if request.method == 'POST':
                    form = ColumnForSorting(cols_list, request.POST or None)
                    if form.is_valid():
                        flag = form.cleaned_data.get("col1")
                        if flag == '0':
                            messages.info(request, "No changes made!")
                            return redirect("user_mgmt:sorting", username=username, filename=filename)
                        else:
                            column_name = cols_list[int(flag)][1]
                            df.sort_values(by=[column_name], inplace=True)
                            f1 = ContentFile(df.to_csv(index=False))
                            file_obj.last_modified = timezone.now()
                            file_obj.uploaded_file.delete()
                            # trying to flag the old file but incase of sorting we do not need a backup
                            file_obj.uploaded_file.save(filename, f1, save=True)
                            messages.success(request, "Data sorted Successfully w.r.t. " + column_name)
                            return redirect("user_mgmt:open_data_file", username=username, filename=filename)

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


def dropna(request, username, filename, action_=None):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar and current_op used to activate siderbar
                current_path = "/media/" + username + "/" + filename 
                current_op = "cleaning"
                # sending datafile with missing values
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                df = general_tool.read_dataframe(file_obj)
                if action_ == "drop_row":
                    # trying to backing up the old file but incase of renaming we do not need a backup
                    general_tool.file_backup(file_obj, "dropping_row", username, filename)
                    # these drops the rows 
                    num_of_rows = len(df)
                    df.dropna(inplace=True)
                    f1 = ContentFile(df.to_csv(index=False))
                    # df.reset_index(drop=True)
                    file_obj.uploaded_file.save(filename, f1, save=True)
                    messages.success(request, str(num_of_rows - len(df)) + " Row(s) dropped successfully!")
                # finding only those rows which contain null values
                # df = df[pd.isnull(df).any(axis=1)]   This will return all rows having missing values
                datatable = datatable_table_creator.converter(df[pd.isnull(df).any(axis=1)], 2) # here 2 tells that width and height should reduced
                return render(request=request, template_name='module2_html/dropna.html', context= {"current_url": current_path, "current_op": current_op, "data_file": datatable})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404

# this support both forward fill as well as backward fill, distinguished by action_
def fill(request, username, filename, action_=None):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar and current_op used to activate siderbar
                current_path = "/media/" + username + "/" + filename 
                current_op = "cleaning"
                # sending datafile with missing values
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                df = general_tool.read_dataframe(file_obj)
                if action_:
                    # trying to backing up the old file for both backfill and forward fill
                    general_tool.file_backup(file_obj, "fbfill", username, filename)
                    if action_ == "forward":
                        df.ffill(axis=0, inplace=True)
                    else:
                        df.bfill(axis=0, inplace=True)
                    # Now trying to save file
                    f1 = ContentFile(df.to_csv(index=False))
                    file_obj.uploaded_file.save(filename, f1, save=True)
                    messages.success(request, "Eligible Data Filled Successfully!")
                datatable = datatable_table_creator.converter(df[pd.isnull(df).any(axis=1)], 2) # here 2 tells that width and height should reduced
                return render(request=request, template_name='module2_html/fill.html', context= {"current_url": current_path, "current_op": current_op, "data_file": datatable})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404

# this support replacing of missing data based on column
# this function uses same form which is used incase of renaming of columns
def replace(request, username, filename, action_=None):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                # current_path gives the url to sidebar and current_op used to activate siderbar
                current_path = "/media/" + username + "/" + filename 
                current_op = "cleaning"
                # sending datafile with missing values
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                df = general_tool.read_dataframe(file_obj)
                cols_list = list(df.columns)
                form_cols_list = list(map(lambda x: " (".join(x) + ")", zip(map(str, cols_list), map(str, df.dtypes))))
                if request.method == 'POST':
                    form = RenameColumnForm(form_cols_list, request.POST or None)
                    if form.is_valid():
                        columns_options = dict(map(lambda x: (x, None), cols_list)) # this dict contain the response of each column
                        # appending data for each response
                        flag = False   # it remains false if no column selected for filling
                        for i in range(1, min(9, len(cols_list)+1)):    # currently we are supporting 8 columns only
                            ch = form.cleaned_data.get('col%s'%i)
                            # checking whether it is empty or not
                            if ch:
                                columns_options[cols_list[i-1]] = ch  # appending the name of given column to be deleted
                                flag = True
                            else:
                                pass    # because None already assigned
                        if flag:
                            for i in columns_options.items():
                                if i[1]:
                                    df[i[0]].fillna(i[1], inplace = True) 
                            # backing up and saving file
                            general_tool.file_backup(file_obj, "ReplaceMissingData", username, filename)
                            f1 = ContentFile(df.to_csv(index=False))
                            file_obj.uploaded_file.save(filename, f1, save=True)
                            messages.success(request, " Data Replaced Successfully!")
                        else:
                            messages.info(request, " No changes made!")
                        return redirect("user_mgmt:replace", username=username, filename=filename)
                # this is coupled with module 3
                datatable = datatable_table_creator.converter(df[pd.isnull(df).any(axis=1)], 2) # here 2 tells that width and height should reduced
                form = RenameColumnForm(form_cols_list) 
                return render(request=request, template_name='module2_html/replace_missing_data.html', context= {"form": form, "current_url": current_path, "current_op": current_op, "data_file": datatable})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module2_html/preprocess.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404

def under_construction(request, username, filename, slug=False):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
                # current_path gives the url to sidebar
                current_path = "/media/" + username + "/" + filename
                if slug: 
                    current_op = "cleaning"
                else:
                    current_op = "combining_dataset"
                messages.info(request, str(slug) + " feature coming soon..")
                return render(request=request, template_name='module2_html/under_construction.html', context= {"current_url": current_path, "current_op": current_op})
    raise Http404