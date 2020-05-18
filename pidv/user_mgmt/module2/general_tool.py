import os
import re
from django.utils import timezone
from django.conf import settings
import pandas as pd
# from user_mgmt.models import Upload_csv

def read_dataframe(file_obj):
    if file_obj.uploaded_file.name.endswith('csv'):
        df = pd.read_csv(file_obj.uploaded_file.path)
    else:
        df = pd.read_excel(file_obj.uploaded_file)
    return df

# Currently this gives a backup for edited file
def file_backup(car, opr, username, filename):
    # car contain Upload_csv object like: <Upload_csv: user_1/new_student_record.csv>
    # car is nothing but file object
    filename = filename.split(".")    # separating filename & extension name
    new_name = "".join(filename[:-1]) + "_" + opr + "_" + re.sub(r'\:|\+|\.', '-', str(timezone.now())) + "." + filename[-1]
    # if there is already a backup file exist then delete existing one
    if car.uploaded_file_backup:
        car.uploaded_file_backup.delete()
    car.uploaded_file_backup.save(new_name, car.uploaded_file, save=True)
    car.uploaded_file.delete()
    car.last_modified = timezone.now()
    car.save()         
    return True