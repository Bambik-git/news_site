from django import forms
from .models import Category


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150,
                            label='Название',
                            initial='Название новости',
                            widget=forms.TextInput(attrs={'class': 'form-control'})
                            )
    content = forms.CharField(label='Текст',
                              required=False,
                              help_text='Что произошло?',
                              widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
                              )
    is_published = forms.BooleanField(label='Опбулиоквано?',
                                      initial=True
                                      )

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      label='Категория',
                                      empty_label='Выберите категорию',
                                      widget=forms.Select(attrs={'class': 'form-control'})
                                      )
