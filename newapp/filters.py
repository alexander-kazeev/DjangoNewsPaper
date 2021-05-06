from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
import django_filters
from django.forms import DateInput


# создаём фильтр
class NewsFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет фильтроваться (т.е. подбираться) информация о постах
    class Meta:
        model = Post
        fields = {
            'postDTCreate':['gt'],
            'postTitle': ['icontains'],
            'postAuthor__authorUser__username': ['icontains'],
        }


# создаём фильтр
class SearchFilter(FilterSet):
    post_dt_create = django_filters.DateFilter(field_name='postDTCreate', widget=DateInput(attrs={'type': 'date'}),
                                            lookup_expr='gt', label='Дата публикации позже')
    post_title = django_filters.CharFilter(field_name='postTitle', lookup_expr='icontains',
                                            label='Название')
    author_name = django_filters.CharFilter(field_name='postAuthor__authorUser__username', lookup_expr='icontains',
                                            label='Автор')

    # class Meta:
    #     model = Post
    #     fields = {
    #         'postDTCreate':['gt'],
    #         'postTitle': ['icontains'],
    #         'postAuthor__authorUser__username': ['icontains'],
    #     }
