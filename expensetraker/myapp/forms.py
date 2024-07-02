from django import forms
from django.contrib.auth.models import User
from .models import Expense
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields=('name','amount','category')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    
    password = forms.CharField(
                                 label='Password',
                                 widget=forms.PasswordInput
                                 )
    password2  = forms.CharField(
                                 label='Confirm password',
                                 widget=forms.PasswordInput
                                 )
    class Meta:
        model = User
        fields = {'username','email','first_name'}
    
    def check_password(self):
        if self.cleaned_data['password']!= self.cleaned_data['password2']:
            raise forms.ValidationError('password do not match')
        return self.cleaned_data['password2']

