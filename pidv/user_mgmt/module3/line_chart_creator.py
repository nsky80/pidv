# This file used to convert df data into line chart compatible data
from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools
from django.contrib import messages


line_chart_template = """
<html>
<head>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

      var data = new google.visualization.DataTable();
          var data = new google.visualization.DataTable(%(json_data)s, 0.6);


// Set chart options

      var options = {
        chart: {
          title: 'Line chart of given Data',
          subtitle: 'Scaling not known'
        },
        width: 865,
        height: 500,
        axes: {
          x: {
            0: {side: 'top'}
          }
        }
      };

      var chart = new google.charts.Line(document.getElementById('line_top_x'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }
  </script>
</head>
<body>
  <div id="line_top_x"></div>
</body>
</html>
"""

def draw_line_chart(original_df, col1, col2, col3, col4, flag=False):
    try:
        # check whether selected rows compatible with pie_chart or not?
        if original_df[col1].dtypes == 'O' or original_df[col2].dtypes == 'O' or original_df[col3].dtypes == 'O' or original_df[col4].dtypes == 'O':
            raise Exception("Selected columns isn't compatible with pie chart, Please select appropriate columns!")
            
        # try to create a new dataframe from existing dataframe
        df = original_df[[col1, col2, col3, col4]].copy()
        columns_ = list(df.columns)
        data_table = general_tools.create_datatable(df)

    #         print("Content-type: text/plain")
    #         print(data_table.ToJSon(columns_order=columns_,
    #                                    order_by=columns_[0]))
        json_data = data_table.ToJSon(columns_order=columns_,
                                order_by=columns_[0])
        return line_chart_template % vars()
    except KeyError:
        raise Exception("Either this column doesn't exist or you have entered wrong column!")
    except Exception as ex:
        raise Exception(ex)
