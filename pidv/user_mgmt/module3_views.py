from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from user_mgmt.models import Upload_csv
# import json
import pandas as pd
# import csv
# import os
from django.conf import settings
from user_mgmt.module3 import pie_chart_creator


def show_graph_options(request, username, filename):
    return render(request, template_name="module3_html/show_graph_options.html")


def pie_chart(request, username, filename):
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
                row1 = "Name"
                row2 = "chemistry"
                pie_graph = pie_chart_creator.draw_pie_chart(df, row1, row2)
                return render(request, template_name="module3_html/draw_pie_chart.html", context={"graph": pie_graph})

            except Exception as ex:
                messages.error(request, ex)
                return HttpResponseRedirect(reverse("user_mgmt:dashboard"))        
    raise Http404
