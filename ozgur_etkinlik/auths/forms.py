from django import forms
from django.contrib.auth import authenticate
import re

from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(required=True, max_length=50, label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('Hatalı kullanıcı adı veya parola girdiniz.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):  # username email formatında mı?
            users = User.objects.filter(email__iexact=username)
            if len(username) > 0 and len(users) == 1:
                return users.first().username
        return username


class RegisterForm(forms.ModelForm):
    password = forms.CharField(required=True, label='Password', min_length=5,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(required=True, label='Password Confirm', min_length=5,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            self.add_error('password', 'Parolalar Eşleşmiyor')
            self.add_error('password_confirm', 'Parolalar Eşleşmiyor')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Böyle bir eposta mevcut')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Böyle bir kullanıcıadı mevcut ')
        return username