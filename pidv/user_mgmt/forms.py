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


class LineChartColumnSelectionForm(forms.Form):
    def __init__(self, nt_x, nt_y, *args,**kwargs): #numeric_type1, numeric_type2, numeric_type3, *args,**kwargs):
        super(LineChartColumnSelectionForm, self).__init__(*args,**kwargs)
        # self.no_of_cols = len(nt_args)
        self.fields['col1'].widget = forms.Select(choices=nt_x)
        # for cnt, dt in enumerate(nt_y, 2):
        cols_available = len(nt_y) + 1
        for i in range(2, 9):
            if i < cols_available:
                self.fields['col%s'%i].widget = forms.Select(choices=nt_y)
            else:
                self.fields['col%s'%i].widget = forms.HiddenInput()
                # self.fields['col%s'%i].disabled = True

    # currently supporting only 8 columns
    col1 = forms.CharField(label="Reference Columns (X-axis)", required=True)
    col2 = forms.CharField(label="Second Numeric Columns (Y-axis)", required=False)
    col3 = forms.CharField(label="Third Numeric Columns (Y-axis)", required=False)
    col4 = forms.CharField(label="Fourth Numeric Columns (Y-axis)", required=False)
    col5 = forms.CharField(label="Fifth Numeric Columns (Y-axis)", required=False)
    col6 = forms.CharField(label="Sixth Numeric Columns (Y-axis)", required=False)
    col7 = forms.CharField(label="Seventh Numeric Columns (Y-axis)", required=False)
    col8 = forms.CharField(label="Eighth Numeric Columns (Y-axis)", required=False)


class RenameColumnForm(forms.Form):
    def __init__(self, cols_list, *args,**kwargs): 
        super(RenameColumnForm, self).__init__(*args,**kwargs)
        cols_available = len(cols_list) 
        for i in range(1, 9):
            if i <= cols_available:
                # pass
                self.fields['col%s'%i].label = cols_list[i-1]
            else:
                self.fields['col%s'%i].widget = forms.HiddenInput()

    col1 = forms.CharField(max_length=30, required=False)
    col2 = forms.CharField(max_length=30, required=False)
    col3 = forms.CharField(max_length=30, required=False)
    col4 = forms.CharField(max_length=30, required=False)
    col5 = forms.CharField(max_length=30, required=False)
    col6 = forms.CharField(max_length=30, required=False)
    col7 = forms.CharField(max_length=30, required=False)
    col8 = forms.CharField(max_length=30, required=False)


class RemoveColumnForm(forms.Form):
    def __init__(self, cols_list, *args,**kwargs): 
        super(RemoveColumnForm, self).__init__(*args,**kwargs)
        cols_available = len(cols_list) 
        for i in range(1, 9):
            if i <= cols_available:
                # pass
                self.fields['col%s'%i].label = cols_list[i-1]
            else:
                self.fields['col%s'%i].widget = forms.HiddenInput()

    col1 = forms.BooleanField(required=False)
    col2 = forms.BooleanField(required=False)
    col3 = forms.BooleanField(required=False)
    col4 = forms.BooleanField(required=False)
    col5 = forms.BooleanField(required=False)
    col6 = forms.BooleanField(required=False)
    col7 = forms.BooleanField(required=False)
    col8 = forms.BooleanField(required=False)


class ColumnForSorting(forms.Form):
    def __init__(self, cols_list, *args,**kwargs):
        super(ColumnForSorting, self).__init__(*args,**kwargs)
        self.fields['col1'].widget = forms.Select(choices=cols_list)

    col1 = forms.CharField(label="Select Column")


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
