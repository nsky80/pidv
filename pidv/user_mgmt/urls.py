from django.urls import path
from user_mgmt import views, module2_views, module3_views

app_name = "user_mgmt"

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login', views.login_request, name="login_request"),
    path('logout', views.logout_request, name="logout_request"), 
    path('register', views.register, name="register"),
    path('help', views.help, name="help"),
    path('feedback', views.feedback, name="feedback"),

    path('dashboard', views.dashboard, name="dashboard"),
    path('account', views.account, name="account"), 
    path('account/edit_profile', views.edit_profile, name="edit_profile"),
    path('contribute', views.contribute, name="contribute"),
    path('community', views.community, name="community"),
    path('upload', views.upload_csv_file, name="upload"),
    path('media/<str:username>/<str:filename>', module2_views.open_data_file, name="open_data_file"),
    path('media/<str:username>/<str:filename>/download', module2_views.download_file, name="download_file"),
    path('media/<str:username>/<str:filename>/preprocess', module2_views.preprocess, name='preprocess'),
    path('media/<str:username>/<str:filename>/delete_file', module2_views.delete_data_file, name='delete_file'),
    path('media/<str:username>/<str:filename>/visualize', module3_views.show_graph_options, name='show_graph_options'),
    path('media/<str:username>/<str:filename>/visualize/pie_chart', module3_views.pie_chart, name='pie_chart'),
    path('media/<str:username>/<str:filename>/visualize/line_chart<int:graph_type>', module3_views.line_chart, name='line_chart1'),
    path('media/<str:username>/<str:filename>/visualize/area_chart<int:graph_type>', module3_views.line_chart, name='area_chart2'),


    path('<slug>', views.under_construction, name="under_construction"),
]
