from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from user_mgmt.models import Upload_csv
# import json
import pandas as pd
# import csv
# import os
from django.conf import settings
from user_mgmt.module3 import datatable_table_creator