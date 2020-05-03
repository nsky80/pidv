"""This file contain some common methods for module3"""
from user_mgmt.module3 import gviz_api
import pandas as pd

# This is used for creating the description or schema for dataframe to datatable convertor
def description_creator(df):
    description= []
    for field, datatype in zip(df.columns, df.dtypes):
        if datatype == 'object':
            dt = "string"
        elif datatype == "bool":
            dt = "boolean"
        else:
            dt = "number"
        description.append((field, dt))
    return description


# This creates the datatable format data for sending to front-end
def create_datatable(df):
    # creating description or schema for dataframe to convert into datatable format
    description = description_creator(df)
#     columns_ = list(df.columns)
#     print("This is description", description)

    data = []
    for index, row in df.iterrows():
        data.append(list(map(lambda x: row[x[0]], description)))

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)
    return data_table
