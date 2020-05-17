from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools


scatter_chart_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    
      google.charts.load('current', {'packages':['corechart', 'scatter']});
      google.charts.setOnLoadCallback(drawStuff);

      function drawStuff() {

        var button = document.getElementById('change-chart');
        var chartDiv = document.getElementById('chart_div');

          var data = new google.visualization.DataTable(%(json_data)s, 0.6);

        var materialOptions = {
          chart: {
            title: 'Scatter plot of given data',
            subtitle: 'based on given y-axis column'
          },
          width: 875,
          height: 500,
          series: {
            0: {axis: '%(y_axis_title1)s'},
            1: {axis: '%(y_axis_title2)s'}
          },
          axes: {
            y: {
              'hours studied': {label: '%(y_axis_title1)s'},
              'final grade': {label: '%(y_axis_title2)s'}
            }
          }
        };

        var classicOptions = {
          width: 880,
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}
          },
          title: 'Scatter plot based on given y-axis data',

          vAxes: {
            // Adds titles to each axis.
            0: {title: '%(y_axis_title1)s'},
            1: {title: '%(y_axis_title2)s'}
          }
        };

        function drawMaterialChart() {
          var materialChart = new google.charts.Scatter(chartDiv);
          materialChart.draw(data, google.charts.Scatter.convertOptions(materialOptions));
          button.innerText = 'Change to Classic';
          button.onclick = drawClassicChart;
        }

        function drawClassicChart() {
          var classicChart = new google.visualization.ScatterChart(chartDiv);
          classicChart.draw(data, classicOptions);
          button.innerText = 'Change to Material';
          button.onclick = drawMaterialChart;
        }

        drawMaterialChart();
    };
    
    
</script>
  </head>
  <body>
    <button id="change-chart" class="waves-effect indigo waves-light btn white-text">Change to Classic</button>
    <br><br>
    <div id="chart_div" style="width: 880px; height: 500px;"></div>

  </body>
</html>
"""


def draw_scatter_chart(original_df, column_list, flag=False):
    try:            
        # try to create a new dataframe from existing dataframe
        df = original_df[column_list[1:]].copy()
        if column_list[0] == "index":
            df.insert(loc=0, column='auto_index', value=list(df.index))
            x_axis_title = 'auto_index'
            # print(list(df.index))
        else:
            x_axis_title = column_list[0]
            df.insert(loc=0, column=column_list[0], value=original_df[column_list[0]])
        y_axis_title1 = column_list[1]
        # since minimum 1 column can be selected
        if len(column_list) > 2:
            y_axis_title2 = column_list[2]
        else:
            y_axis_title2 = column_list[1]

        columns_ = list(df.columns)
        data_table = general_tools.create_datatable(df)
        json_data = data_table.ToJSon(columns_order=columns_,
                                order_by=columns_[0])
        return scatter_chart_template % vars()
    except KeyError:
        raise Exception("Either this column doesn't exist or you have entered wrong column!")
    except Exception as ex:
        raise Exception(ex)
