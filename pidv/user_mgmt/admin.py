from django.contrib import admin
from .models import Feedback, Upload_csv

# Register your models here.
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('feedback_title', 'feedback_user_id', 'feedback_date')   # displays the info in row
    list_filter = ['feedback_user_id', 'feedback_date']
    # search_fields = ['essay_title', 'series_title']
    ordering = ['feedback_date']

    fieldsets = [
        ("Title/date", {'fields': ["feedback_title", "feedback_date", "feedback_user_id",]}),
        ("Content", {'fields': ['feedback_content']}),
    ]

class Upload_csvAdmin(admin.ModelAdmin):
    list_display = ("view_file_name", "user", "uploaded_on", "last_modified")   # displays the info in row
    list_filter = ['user', 'uploaded_on']
    # search_fields = ["foreign_key__user"]
    # ordering = ['series_title']

    fieldsets = [
       
        ("User", {'fields': ["user"]}),
        ("Content", {"fields": ["uploaded_file"]}),
        ("Last Backup", {"fields": ["uploaded_file_backup"]}),
        ("Timeline", {'fields': ["uploaded_on", "last_modified", ]}),
    ]
    def view_file_name(self, obj):
        return obj.uploaded_file.name



# Register your models here.
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Upload_csv, Upload_csvAdmin)