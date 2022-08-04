from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.db.models import *

from .serializers import *
from rest_framework import generics, status, views

from mysite.settings import EMAIL_HOST_USER
from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm


class HomeNews(ListView):
    """ Список всех опубликованных новостей """
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(ListView):
    """  Список новостей опрделенных категорий """
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'],
                                   is_published=True)  # WHERE category_id AND is_published

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context


class ViewNews(DetailView):
    """ Вывод полного теста определенной новости"""
    model = News
    template_name = 'news/news_view.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['news'].title
        return context

    def get_queryset(self):
        qs = News.objects.filter(pk=self.kwargs['pk']).select_related('category')
        return qs


class CreateNews(LoginRequiredMixin, CreateView):
    """ Создание новости """

    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = reverse_lazy('home')
    raise_exception = True


class Search(ListView):
    model = News
    template_name = 'news/search.html'
    context_object_name = 'news'

    def get_queryset(self):
        q = self.request.GET.get('q')
        return News.objects.filter(is_published=True, title__contains=q).select_related('category')


"""
                #####################################
                #                                   # 
                #        function based View        #
                #                                   #
                #####################################       
"""


def register(request):
    """ Регистрация пользователя и добавление в группу "Пользователи" """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            group = Group.objects.get(pk=1)
            group.user_set.add(user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Увы, произошла ошибка регистрации!')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    """ Аутентификация пользователя """
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('user_login', user)
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    """ Выход пользователя """
    logout(request)
    return redirect('home')


def sending_mail(request):
    """ Обратная связь """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['context'],
                             EMAIL_HOST_USER, 'Elfuses@gmail.com', fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('test')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/send_mail.html', {'form': form})


"""
                #####################################
                #                                   # 
                #                API                #
                #                                   #
                #####################################       
"""


class NewsListDetail(generics.ListAPIView):
    """ API вывода конкретной новости """
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(pk=self.kwargs['id'], is_published=True)


class NewsList(generics.ListAPIView):
    """ Вывод списка всех новостей """
    queryset = News.objects.filter(is_published=True).select_related('category')
    serializer_class = NewsSerializer


class APINewsByCategory(generics.ListAPIView):
    """ Получение всех новостей определенной категории"""
    serializer_class = NewsByCategorySerializer

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)

