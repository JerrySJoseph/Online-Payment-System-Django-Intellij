from django import forms
from iam.forms import username_validator,email_validator
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from crispy_forms.bootstrap import Field


class EditProfileForm(forms.Form):

    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: John'}), required=True,)
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: Doe'}), required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: JohnDoe123',}), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: john.doe@gmail.com'}), required=True, validators=[
        EmailValidator(message='Invalid email')])

    current_user:User=None

    def __init__(self,current_user:User,*args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        if current_user:
            self.fields['firstname'].initial=current_user.first_name
            self.fields['lastname'].initial=current_user.last_name
            self.fields['username'].initial=current_user.username
            self.fields['email'].initial=current_user.email
            self.current_user=current_user



    def save(self):
        self.current_user.username=self.cleaned_data['username']
        self.current_user.first_name=self.cleaned_data['firstname']
        self.current_user.last_name=self.cleaned_data['lastname']
        self.current_user.email=self.cleaned_data['email']
        self.current_user.save()
        return self.current_user
        


