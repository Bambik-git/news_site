from django.conf.urls.static import static
from django.urls import path, include
from mysite import settings
from .views import *


urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('<int:pk>/', ViewNews.as_view(), name='news_view'),
    path('add_news/', CreateNews.as_view(), name='add_news'),
    path('sending_mail/', sending_mail, name='sending_mail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('search', Search.as_view(), name='search'),

    path('api/news_view/', NewsList.as_view(), name='api_news'),
    path('api/news/<int:id>', NewsListDetail.as_view(), name='api_news_view'),
    path('api/category/<int:category_id>', APINewsByCategory.as_view(), name='api_category')

]

