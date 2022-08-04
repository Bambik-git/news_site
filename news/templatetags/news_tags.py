import datetime

from django import template
from django.db.models import *
from news.models import Category, News
from django.core.cache import cache

register = template.Library()


@register.simple_tag(name='top3_news')
def get_top3_news_of_the_week():
    ''' Получение топ 3 новости за неделю и кеширование на 6 часов '''
    top3_news = cache.get('top3_news')
    if top3_news:
        top3_news = News.objects \
                        .filter(created_at__gt=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)) \
                        .order_by('-views')[:3]
        cache.set('top3_news', top3_news, 6*60*60)
    return top3_news


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    """ Получение списка категорий и кеширование на 3 часа """
    categories = cache.get('categories')
    if not categories:
        categories = Category.objects.annotate(cnt=Count('get_news', filter=F('get_news__is_published'))).\
                                        filter(cnt__gt=0)
        cache.set('categories', categories, 3*60*60)
    return {'categories': categories}


