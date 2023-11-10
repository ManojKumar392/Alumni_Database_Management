from django import forms
from .models import Alumni
from .models import JobOpening
from .models import Work

class QueryForm(forms.Form):
    select_field = forms.CharField(label='SELECT', required=False)
    insert_field = forms.CharField(label='INSERT', required=False)
    update_field = forms.CharField(label='UPDATE', required=False)
    delete_field = forms.CharField(label='DELETE', required=False)

class UserInputForm(forms.Form):
    user_input = forms.CharField(
        label='Enter query:',
        widget=forms.Textarea(attrs={'rows': 10, 'cols': 40}) 
    )

class NameForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    subject = forms.CharField(max_length=200, label='Subject')
    message = forms.CharField(widget=forms.Textarea, label='Message')

class LoginForm(forms.Form):
    password = forms.CharField(label="SRN")
    passkey = forms.CharField(widget=forms.PasswordInput)

class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AlumniForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = ['title', 'description', 'application_deadline', 'alumni']