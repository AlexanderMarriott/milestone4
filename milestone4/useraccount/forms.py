from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

# registration form

class UserAccountForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserAccountForm, self).__init__(*args, **kwargs)


        # set email field to required
        self.fields['email'].required = True


    # Validate the email field

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        
        if len (email) <= 6:
            raise forms.ValidationError("Email is too short")
        elif len(email) >= 150:
            raise forms.ValidationError("Email is too long")
        return email
    
#login form

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
    

# update form

class UserUpdateForm(forms.ModelForm):

    password = None

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)


        # set email field to required
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ["username", "email"]
        exclude = ['password1', 'password2']