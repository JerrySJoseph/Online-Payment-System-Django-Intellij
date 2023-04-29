
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.core.validators import EmailValidator
from django import forms
from django.utils.translation import gettext_lazy as _
from iam.api.register import check_email_exists, check_username_exists


# validate email field
def email_validator(email):
    if check_email_exists(email=email):
        raise forms.ValidationError('A user exists with this email id.')

# validate username field


def username_validator(username):
    if check_username_exists(username=username):
        raise forms.ValidationError(_('A user exists with username : %(invalid_username)s'), params={
            'invalid_username': username
        })

# validate password field


def password_validator(password):
    if len(password) < 5:
        raise forms.ValidationError('Password is too short')


# Form Manager for Register page
class RegisterForm(forms.Form):
    firstname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: John'}), required=True,)
    lastname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: Doe'}), required=True)
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: JohnDoe123'}), required=True, validators=[username_validator])
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: john.doe@gmail.com'}), required=True, validators=[
                            email_validator, EmailValidator(message='Invalid email')])
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, validators=[password_validator])
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(), required=True)
    tnc_check = forms.BooleanField(
        required=False, label='I accept Terms and conditions')
    is_superuser: bool = False

    def __init__(self, is_superuser: bool = False, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.is_superuser = is_superuser

    # override default form.clean function for custom validations

    def clean(self):
        cleaned_data = super().clean()

        # check whether both passwords match
        password_input = cleaned_data.get('password')
        confirm_password_input = cleaned_data.get('confirm_password')

        # add error to form field if passwords do not match
        if password_input != confirm_password_input:
            self.add_error('confirm_password', 'Passwords do not match')

        if not self.is_superuser and cleaned_data.get('tnc_check') == False:
            self.add_error(
                'tnc_check', 'You need to accept Terms and Conditions first.')
        

    def save(self, is_admin: bool = False):
        username = self.cleaned_data['username']
        firstname = self.cleaned_data['firstname']
        lastname = self.cleaned_data['lastname']
        email = self.cleaned_data['email']
        password = self.cleaned_data['confirm_password']
        user_creation_fn = User.objects.create_superuser if is_admin else User.objects.create_user
        user = user_creation_fn(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Eg: JohnDoe123'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, validators=[password_validator])

  

    def clean(self):
        cleaned_data = super().clean()
        if not check_username_exists(cleaned_data['username']):
            self.add_error('username', 'No user with this username exists.')
