from django import forms 
from .models import Feedback, Upload_csv
# from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


# User can modify his information and it allows only what user can modify
class EditProfileForm(UserChangeForm):
     class Meta:
         model = User
         fields = (
             'username',
             'email',
             'first_name',
             'last_name',
         )
        #  exclude = ()


# This is feedback form which is open to all but id required
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('feedback_title', 'feedback_user_id', 'feedback_content')


class Upload_csvForm(forms.ModelForm): 
    class Meta: 
        model = Upload_csv 
        fields = [
        'uploaded_file', 
        ] 


class ColumnSelectionForm(forms.Form):

    def __init__(self, string_type, numeric_type, *args,**kwargs):
        super(ColumnSelectionForm, self).__init__(*args,**kwargs)
        self.fields['col1'].widget = forms.Select(choices=string_type)
        self.fields['col2'].widget = forms.Select(choices=numeric_type)

    col1 = forms.CharField(label="String Columns" )
    col2 = forms.CharField(label="Numeric Columns")




# This class is added only for testing purposes it will remove soon!
class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')
