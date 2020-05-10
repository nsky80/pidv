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

                numeric_type1 = [('0', 'Select First Column')]
                numeric_type2 = [('0', 'Select Second Column')]
                numeric_type3 = [('0', 'Select Third Column')]
                numeric_type4 = [('0', 'Select Fourth Column')]

                for data_ in schema:
                    if data_[1] == 'number':
                        numeric_type1.append((str(len(numeric_type1)), data_[0]))
                        numeric_type2.append((str(len(numeric_type1)), data_[0]))
                        numeric_type3.append((str(len(numeric_type1)), data_[0]))
                        numeric_type4.append((str(len(numeric_type1)), data_[0]))

                if request.method == 'POST':
                    form = LineChartColumnSelectionForm(numeric_type1, numeric_type2, numeric_type3, numeric_type4, request.POST)
                    if form.is_valid():
                        col1 = numeric_type1[int(form.cleaned_data.get('col1'))][1]
                        col2 = numeric_type2[int(form.cleaned_data.get('col2'))][1]
                        col3 = numeric_type1[int(form.cleaned_data.get('col3'))][1]
                        col4 = numeric_type2[int(form.cleaned_data.get('col4'))][1]
                        line_graph = line_chart_creator.draw_line_chart(df, col1, col2, col3, col4)
                        return render(request, template_name="module3_html/draw_pie_chart.html", context={"graph": line_graph})

                form = LineChartColumnSelectionForm(numeric_type1, numeric_type2, numeric_type3, numeric_type4)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
            except Exception as ex:
                messages.error(request, ex)
                return render(request=request, template_name='module3_html/draw_pie_chart_options.html', context= {'form':form})
    raise Http404
