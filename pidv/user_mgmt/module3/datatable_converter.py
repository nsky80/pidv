
from user_mgmt.module3 import gviz_api
import pandas as pd

page_template = """
<html>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1', {packages:['table']});

    google.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode)s
      var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
      jscode_table.draw(jscode_data, {showRowNumber: true});

      var json_table = new google.visualization.Table(document.getElementById('table_div_json'));
      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
      json_table.draw(json_data, {showRowNumber: true});
    }
  </script>
  <body>

    <div id="table_div_jscode"></div>
  </body>
</html>
"""

def converter(df):
  # Creating the data
    # df = pd.read_csv('D:\\Project IDV\\Jupyter\\Datasets\\student_data.csv')
    columns_ = tuple(df.columns)
    description = list(map(lambda x: (x,), columns_))
    data = []
    for index, row in df.iterrows():
        data.append(list(map(lambda x: row[x[0]], description)))

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Create a JavaScript code string.
    jscode = data_table.ToJSCode("jscode_data",
                               columns_order=columns_,
                               order_by=columns_[0])
    # Create a JSON string.
    json = data_table.ToJSon(columns_order=columns_,
                           order_by=columns_[0])

    # Put the JS code and JSON string into the template.
    #   print "Content-type: text/html"
    #   print
    result = page_template % vars()
    # print(result)
    return result



