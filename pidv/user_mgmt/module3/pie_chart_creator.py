# This file used to convert df data into pie chart compatible data
from user_mgmt.module3 import gviz_api
import pandas as pd
from user_mgmt.module3 import general_tools
from django.contrib import messages

pie_chart_template = """
<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">

          // Load the Visualization API and the piechart package.
      google.charts.load('current', {'packages':['corechart']});

      // Set a callback to run when the Google Visualization API is loaded.
      google.charts.setOnLoadCallback(drawChart);

      // Callback that creates and populates a data table, 
      // instantiates the pie chart, passes in the data and
      // draws it.
      function drawChart() {

      // Create the data table.
    var data = new google.visualization.DataTable(%(json_data)s, 0.6);


// Set chart options
      var options = {'title':'Pie Chart for given columns',
                     'width':400,
                     'height':300};

      // Instantiate and draw our chart, passing in some options.
      var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }
    </script>
  </head>

  <body>
<!--Div that will hold the pie chart-->
    <div id="chart_div" style="width:400; height:300"></div>
  </body>
</html>
"""

def draw_pie_chart(original_df, row1, row2, flag=False):
    try:
        # check whether selected rows compatible with pie_chart or not?
        if not original_df[row1].dtypes == 'O':
            raise Exception("Selected columns isn't compatible with pie chart, Please select appropriate columns!")
            
        # try to create a new dataframe from existing dataframe
        df = original_df[[row1, row2]].copy()
        columns_ = list(df.columns)
        data_table = general_tools.create_datatable(df)

#         print("Content-type: text/plain")
#         print(data_table.ToJSon(columns_order=columns_,
#                                    order_by=columns_[0]))
        json_data = data_table.ToJSon(columns_order=columns_,
                               order_by=columns_[0])
        return pie_chart_template % vars()
    except KeyError:
        raise Exception("Either this column doesn't exist or you have entered wrong column!")
    except Exception as ex:
        raise Exception(ex)
    
