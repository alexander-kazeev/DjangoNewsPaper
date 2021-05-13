from django.forms import ModelForm
from .models import Post
from django import forms


# Создаём модельную форму
class PostForm(ModelForm):
    postText = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control mb-2'}))

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['postAuthor',
                  'postType',
                  'postCategory',
                  'postTitle',
                  'postText',
        ]

        labels = {
            'postAuthor': 'Автор',
            'postType': 'Тип',
            'postCategory': 'Категория',
            'postTitle': 'Заголовок',
        }
