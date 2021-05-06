from django.urls import path
from .views import NewsList, NewsDetail, SearchList, PostDetailView, PostAddView, \
    PostDeleteView, PostEditView  # импортируем наше представление

urlpatterns = [
    path('', NewsList.as_view()),
    # path('<int:pk>', NewsDetail.as_view()),
    path('<int:pk>', PostDetailView.as_view(), name='news_detail'),
    path('search/', SearchList.as_view(), name='news_search'),
    path('add/', PostAddView.as_view(), name='news_add'),
    path('<int:pk>/edit', PostEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='news_delete'),
]