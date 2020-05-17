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
    # this is initial path of file, car is nothing but file object
    initial_path = car.uploaded_file.path
    car.uploaded_file.name = username  + "_" + filename[:-4] + "_" + opr + "_" + re.sub(r'\:|\+|\.', '-', str(timezone.now())) + ".csv"
    # print(re.sub(r'\:|\+|\.', '-', st))    
    # '{0}/{1}/{2}'.format(username, "flagged",filename)
    new_path = settings.MEDIA_ROOT + car.uploaded_file.name
    # print(new_path, type(new_path))
    os.rename(initial_path, new_path)
    car.last_modified = timezone.now()
    car.save()         
    return True