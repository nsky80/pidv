# This file used to convert df data into chart table compatible data
from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools

table_page_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
    var data = new google.visualization.DataTable(%(json_data)s, 0.6);

        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, {showRowNumber: true,
        width: 880,
        height: 500,
        page: 'enable',
        pageSize: 15,
        pagingSymbols: {
            prev: 'prev',
            next: 'next'
        },
        pagingButtonsConfiguration: 'auto'});
      }

    </script>
  </head>
  <body>
    <div id="table_div"></div>
  </body>
</html>

    """

def converter(df):
    # Creating the data
    # df = pd.read_csv('D:\\Project IDV\\Jupyter\\Datasets\\student_data.csv')
    # columns_ = tuple(df.columns)
    # description = description_creator(df)
    # data = []
    # for index, row in df.iterrows():
    #     data.append(list(map(lambda x: row[x[0]], description)))

    # # Loading it into gviz_api.DataTable
    # data_table = gviz_api.DataTable(description)
    # data_table.LoadData(data)

    # creating datatable format from dataframe
    columns_ = tuple(df.columns)
    data_table = general_tools.create_datatable(df)
    # Create a JSON string.
    json_data = data_table.ToJSon(columns_order=columns_,
                            order_by=columns_[0])

    # Put JSON string into the template.

    return table_page_template % vars()



