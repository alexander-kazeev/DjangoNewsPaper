from django.shortcuts import render

from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Post


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsDetail(DetailView):
    model = Post  # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news_one.html'  # название шаблона будет post.html
    context_object_name = 'news_one'  # название объекта. в нём будет