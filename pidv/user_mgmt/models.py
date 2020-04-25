from django.db import models
from django.utils import timezone

# Create your models here.
# Feedback Database, since it is open for all that's why doesn't used User as foreign key
class Feedback(models.Model):
	feedback_title = models.CharField(max_length=100)
	feedback_date = models.DateTimeField("Feedback Time", default=timezone.now)
	feedback_content = models.TextField(help_text="Share Your Ideas Here!")
	feedback_user_id = models.EmailField("Email ID")