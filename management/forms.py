from django import forms
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class WishListForm(forms.Form):
    company = forms.CharField(max_length=200)
    job_title = forms.CharField(max_length=200)

class AppliedForm(forms.Form):
    company = forms.CharField(max_length=200)
    job_title = forms.CharField(max_length=200)
    applied = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(attrs={'type': 'date'}))

class JobInfoForm(forms.Form):
    company = forms.CharField(max_length=200)
    job_title = forms.CharField(max_length=200)
    applied = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    deadline = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    location = forms.CharField(max_length=200,required=False)
    salary = forms.IntegerField(required=False)
    post_url = forms.URLField(max_length=2000,required=False)
    status = forms.CharField(widget=forms.Textarea(),required=False)
    offer = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)

class TaskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea())
    date = forms.DateField(initial=datetime.date.today,widget=forms.DateInput(attrs={'type': 'date'}))
