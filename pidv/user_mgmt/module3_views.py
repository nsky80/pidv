from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from user_mgmt.models import Upload_csv
# import json
from user_mgmt.forms import ColumnSelectionForm, LineChartColumnSelectionForm
import pandas as pd
# import csv
# import os
from django.conf import settings
from user_mgmt.module3 import pie_chart_creator, general_tools, line_chart_creator


def show_graph_options(request, username, filename):
    return render(request, template_name="module3_html/show_graph_options.html")


def pie_chart(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                # it returns the header of csv along with datatype. eg.('Name', 'string'), ('physics', 'number')
                schema = general_tools.description_creator(df)
                string_type = [('0', 'Select String Type')]
                numeric_type = [('0', 'Select Numeric Type')]
                for data_ in schema:
                    if data_[1] == 'string':
                        string_type.append((str(len(string_type)), data_[0]))
                    elif data_[1] == 'number':
                        numeric_type.append((str(len(numeric_type)), data_[0]))
                    else:
                        pass
                if request.method == 'POST':
                    form = ColumnSelectionForm(string_type, numeric_type, request.POST)
                    if form.is_valid():
                        col1 = string_type[int(form.cleaned_data.get('col1'))][1]
                        col2 = numeric_type[int(form.cleaned_data.get('col2'))][1]
                        pie_graph = pie_chart_creator.draw_pie_chart(df, col1, col2)
                        return render(request, template_name="module3_html/draw_pie_chart.html", context={"graph": pie_graph})

                form = ColumnSelectionForm(string_type, numeric_type)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
    raise Http404



def line_chart(request, username, filename):
    if request.user.is_authenticated:
		# checking whether user is opening its own file or not
        if "user_" + str(request.user.id) == username:
            try:
                file_obj = Upload_csv.objects.get(uploaded_file=username+'/'+filename)
                if file_obj.uploaded_file.name.endswith('csv'):
                    df = pd.read_csv(file_obj.uploaded_file)
                else:
                    df = pd.read_excel(file_obj.uploaded_file)
                # it returns the header of csv along with datatype. eg.('Name', 'string'), ('physics', 'number')
                schema = general_tools.description_creator(df)
                # nt stands for numeric type and contains columns in form of options
                nt_x = [('0', 'Select Column for X-axis (Reference axis)'), ('1', 'Index(Auto Generated)')]
                nt_y = [('0', 'Select Column for Y-axis(Otherwise Leave blank)')]
                for data_ in schema:
                    if data_[1] == 'number':
                        nt_x.append((str(len(nt_x)), data_[0]))
                        nt_y.append(((str(len(nt_y)), data_[0])))

                if request.method == 'POST':
                    form = LineChartColumnSelectionForm(nt_x, nt_y, request.POST)
                    if form.is_valid():
                        columns_options = [int(form.cleaned_data.get('col1'))] # for x-axis
                        if columns_options[0] == 0:
                            raise Exception("Reference axis (X-axis) required!")
                        # appending data for y-axis
                        for i in range(2, 9):
                            columns_options.append(int(form.cleaned_data.get('col%s'%i)))
                        # checking whether x-axis is default(index ie auto) or not
                        if columns_options[0] == 1:
                            cols_list = ["index"]
                        else:
                            cols_list = [nt_x[columns_options[0]][1]]  # appending x-axis
                        for i in range(1, 8):   # checking and appending y-axis
                            if columns_options[i] != 0:
                                cols_list.append(nt_y[columns_options[i]][1])
                        if len(cols_list) == 1:
                            raise Exception("Select atleast 1 column for y-axis")
                        line_graph = line_chart_creator.draw_line_chart(df, cols_list)
                        return render(request, template_name="module3_html/draw_pie_chart.html", context={"graph": line_graph})

                form = LineChartColumnSelectionForm(nt_x, nt_y) #, numeric_type4)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
    raise Http404
