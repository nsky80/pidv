# This file used to convert df data into chart table compatible data
from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools

table_page_template = """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
    var data = new google.visualization.DataTable(%(json_data)s, 0.6);

        var table = new google.visualization.Table(document.getElementById('table_div%(divison)d'));

        table.draw(data, {showRowNumber: true,
        %(measure)s
        page: 'enable',
        pagingSymbols: {
            prev: 'prev',
            next: 'next'
        },
        pagingButtonsConfiguration: 'auto'});
      }

    </script>
    <div id="table_div%(divison)d"></div>
    """

stats_page_template = """
    <script type="text/javascript">

      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
    var data = new google.visualization.DataTable(%(json_data)s, 0.6);

        var table = new google.visualization.Table(document.getElementById('table_div%(divison)s'));

        table.draw(data, {showRowNumber: true,
        %(measure)s
        page: 'enable',
        pagingSymbols: {
            prev: 'prev',
            next: 'next'
        },
        pagingButtonsConfiguration: 'auto'});
      }

    </script>
    <div id="table_div%(divison1)s"></div>
    """

def converter(df, type_=1):
    # creating datatable format from dataframe
    columns_ = tuple(df.columns)
    data_table = general_tools.create_datatable(df)
    # Create a JSON string.
    json_data = data_table.ToJSon(columns_order=columns_)
    # divison variable tells which table it is either stats or datatable
    divison = 1
    if type_ == 1:
        measure = "height: 'auto',width: '875', pageSize: 20,"
    elif type == 2:      # this is only for missing values
        measure = 'width: 875, pageSize: 5,'
    else:
        divison = 2
        measure = "height: 'auto',width: '875', pageSize: 20,"
    # Put JSON string into the template.
    return table_page_template % vars()



