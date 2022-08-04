import re

from django import forms
from .models import Category, News
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'categoty': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        """ Валидация поля title Не должно начинаться с числа! """
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Не должно начинаться с цифры', code='invalid')
        return title


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               help_text='Имя пользователя на латинскими буквами. Максимум 50 символов',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        """ Валидация логина. Не менее 3-х символов """
        username = self.cleaned_data['username']
        print(len(username))
        print(username)
        if len(username) < 4:
            raise ValidationError('Короткое имя пользователя! Меньше 3-х символов')
        return username


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    context = forms.CharField(label='Текст',
                               widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

