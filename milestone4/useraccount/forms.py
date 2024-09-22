from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django import forms


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