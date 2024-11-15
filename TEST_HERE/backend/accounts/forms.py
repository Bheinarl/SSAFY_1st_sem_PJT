from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomSignupForm(UserCreationForm):
    nickname = forms.CharField(max_length=50, required=True, label="별명")
    age = forms.IntegerField(required=False, label="나이")
    interests = forms.CharField(widget=forms.Textarea, required=False, label="관심사")

    class Meta:
        model = CustomUser
        fields = ['username', 'nickname', 'age', 'interests', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
