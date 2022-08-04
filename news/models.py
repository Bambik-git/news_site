from django.db import models
from django.db.models import Manager
from django.urls import reverse


class News(models.Model):
    """ Новости """
    title = models.CharField(max_length=150,
                             verbose_name='Наименование'
                             )
    content = models.TextField(blank=True,
                               verbose_name='Контент'
                               )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата публикации'
                                      )
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Изменено'
                                      )
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/',
                              verbose_name='Фото',
                              blank=True
                              )
    is_published = models.BooleanField(default=True,
                                       verbose_name='Опубликовано'
                                       )
    category = models.ForeignKey('Category',
                                 on_delete=models.RESTRICT,
                                 null=True,
                                 verbose_name='Категория',
                                 related_name='get_news'
                                 )
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_view', kwargs={'pk': self.pk})

    def counter(self):
        self.views += 1
        self.save()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at', 'title']


class Category(models.Model):
    """ Категории новостей """
    title = models.CharField(max_length=150,
                             db_index=True,
                             verbose_name='Наименование')

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

