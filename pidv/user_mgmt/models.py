from django.db import models
from django.utils import timezone
from django.conf import settings 
# from django.contrib.auth.models import User

# Create your models here.
# Feedback Database, since it is open for all that's why doesn't used User as foreign key
User = settings.AUTH_USER_MODEL 



class Feedback(models.Model):
	feedback_title = models.CharField(max_length=100)
	feedback_date = models.DateTimeField("Feedback Time", default=timezone.now)
	feedback_content = models.TextField(help_text="Share Your Ideas Here!")
	feedback_user_id = models.EmailField("Email ID")
	class Meta:
		verbose_name_plural = "Feedback"
	
	def __str__(self):
		return self.feedback_title

def user_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
	return "media/" + 'user_{0}/{1}'.format(instance.user.id, filename)

class Upload_csv(models.Model):
	# user = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
	user = models.ForeignKey(User, 
					default = 1, 
					null = True,  
					on_delete = models.SET_NULL 
					) 

	uploaded_file = models.FileField(upload_to=user_directory_path)
	class Meta:
		verbose_name_plural = "Upload_CSV"
	
	def __str__(self):
		return self.uploaded_file.name