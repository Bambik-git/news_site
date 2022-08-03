from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('<int:pk>/', ViewNews.as_view(), name='news_view'),
    path('add_news/', CreateNews.as_view(), name='add_news'),

]
