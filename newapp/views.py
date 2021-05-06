from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import request
from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, \
    UpdateView, DeleteView  # импортируем класс получения деталей объекта
from .models import Post
from .filters import NewsFilter, SearchFilter # импортируем недавно написанный фильтр
from .forms import PostForm # импортируем нашу форму


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    # queryset = Post.objects.order_by('-postDTCreate')
    ordering = ['-postDTCreate']
    paginate_by = 10 # поставим постраничный вывод в 10 элементов
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил то сохраняем новый пост
            form.save()

        return super().get(request, *args, **kwargs)


# дженерик для получения деталей о посте
class PostDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'news_detail'


# дженерик для создания объекта. Надо указать только имя шаблона и класс формы. Остальное он сделает за вас
class PostAddView(CreateView):
    template_name = 'news_add.html'
    form_class = PostForm
    # context_object_name = 'news_add'


# дженерик для редактирования поста
class PostEditView(UpdateView):
    template_name = 'news_add.html'
    # ??? template_name = 'news_edit.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'news_delete'
    success_url = '/news/'


class SearchList(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    # queryset = Post.objects.order_by('-postDTCreate')
    # ordering = ['-postDTCreate']

    paginate_by = 10 # поставим постраничный вывод в 10 элементов

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        post_list = SearchFilter(self.request.GET, queryset=Post.objects.all()).qs.order_by('-postDTCreate')
        paginator = Paginator(post_list, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            post_filter = paginator.page(page)
        except PageNotAnInteger:
            post_filter = paginator.page(1)
        except EmptyPage:
            post_filter = paginator.page(paginator.num_pages)
        context['all_news'] = Post.objects.all()
        context['filter'] = SearchFilter(self.request.GET, queryset=super().get_queryset())
        context['post_list'] = post_filter
        context['filterset'] = post_filter
        return context

    # def get_context_data(self,**kwargs):
    # # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = SearchFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
    #     return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_one.html'
    context_object_name = 'news_one'