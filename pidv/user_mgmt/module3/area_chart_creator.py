from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools

area_chart_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

          var data = new google.visualization.DataTable();
          var data = new google.visualization.DataTable(%(json_data)s, 0.6);

        var options = {
          title: 'Area Chart of Given Data',
          hAxis: {title: '%(x_axis_title)s',  titleTextStyle: {color: '#333'}},
          vAxis: {minValue: 0}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 880px; height: 500px;"></div>
  </body>
</html>
"""


def draw_area_chart(original_df, column_list, flag=False):
    try:            
        # try to create a new dataframe from existing dataframe
        df = original_df[column_list[1:]].copy()
        # if this is auto column
        if column_list[0] == "index":
            df.insert(loc=0, column='auto_index', value=range(1, len(df) + 1))
            x_axis_title = 'auto_index'
            # print(list(df.index))
        else:
            x_axis_title = column_list[0]
            df.insert(loc=0, column=column_list[0], value=original_df[column_list[0]])

        columns_ = list(df.columns)
        data_table = general_tools.create_datatable(df)
        json_data = data_table.ToJSon(columns_order=columns_,
                                order_by=columns_[0])
        return area_chart_template % vars()
    except KeyError:
        raise Exception("Either this column doesn't exist or you have entered wrong column!")
    except Exception as ex:
        raise Exception(ex)
