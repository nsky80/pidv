from django.contrib import admin
from .models import Feedback

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

# Register your models here.
admin.site.register(Feedback, FeedbackAdmin)