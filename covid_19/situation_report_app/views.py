from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail


from django.views.generic import ListView, DetailView, CreateView
from .models import Article, Post, Statistic, Source
from .forms import ContactForm
from situation_report_app.update_statistic import update_statistic
from situation_report_app.update_articles_ru import update_articles
import datetime


# ListView # все данные с кнопкой обновления
class StatisticListView(ListView):
    model = Statistic
    template_name = 'situation_report_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Statistic.objects.first():
            context['updated_on'] = Statistic.objects.first().date
        else:
            context['updated_on'] = datetime.date.today()

        return context

    def post(self, request):
        update_statistic()
        statistic = Statistic.objects.all()
        updated_on = Statistic.objects.first().date

        return render(request, self.template_name, context={'object_list': statistic,
                                                            'updated_on': updated_on,
                                                            })


# все новости
class NewsListView(ListView):
    model = Article
    template_name = 'situation_report_app/news.html'
    ordering = ['-date']
    paginate_by = 5
    # если хотим изменить имя  object_list
    # context_object_name = 'news_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['news_title'] = 'news'
        context['news_line'] = 'from all the World'
        return context

    def post(self, request):
        update_articles()
        articles = Article.objects.order_by('-date')
        return render(request, self.template_name, context={'object_list': articles})


class PostListView(ListView):
    model = Post
    template_name = 'situation_report_app/posts.html'

    def get_queryset(self):

        # вариант без ApprovedManager
        # return Post.objects.filter(is_approved=True)

        # вариант с ApprovedManager
        return Post.approved_objects.all()


class SourceListView(ListView):
    model = Source
    template_name = 'situation_report_app/sources.html'
    paginate_by = 5


# просмотр всех статей от источника (вызывается с помощью pk)
class SourceNewsListView(ListView):
    model = Article
    template_name = 'situation_report_app/source_news.html'

    def get(self, request, *args, **kwargs):
        self.source_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        articles = Article.objects.filter(source=self.source_id)
        context['source_name'] = articles[0].source
        context['source_url'] = articles[0].source.url
        return context

    def get_queryset(self):
        return Article.objects.filter(source=self.source_id)


# DetailView для поста
class PostDetailView(UserPassesTestMixin, DetailView):
    model = Post
    template_name = 'situation_report_app/post_detail.html'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('users:login')

    def get(self, request, *args, **kwargs):
        self.post_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return get_object_or_404(Post, pk=self.post_id)


# CreateView for article
class ArticleCreateView(CreateView):
    # form_class =
    fields = '__all__'
    # fields = 'url',
    model = Article
    success_url = reverse_lazy('covid_19:news')
    template_name = 'situation_report_app/add_article.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


# добавление поста
class PostCreateView(LoginRequiredMixin, CreateView):
    fields = '__all__'
    fields = ('name', 'text', 'image')
    model = Post
    success_url = reverse_lazy('covid_19:posts')
    template_name = 'situation_report_app/create_post.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


# добавление source
class SourceCreateView(CreateView):
    fields = '__all__'
    model = Source
    success_url = reverse_lazy('covid_19:sources')
    template_name = 'situation_report_app/add_source.html'

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


# форма для отправки почты
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail(f'Subject {name}',
                      f'Thank you for your message {message}',
                      'from@example.com',
                      [email],
                      fail_silently=True,
                      )
            return HttpResponseRedirect(reverse('covid_19:index'))
        else:
            return render(request, 'situation_report_app/contact.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'situation_report_app/contact.html', context={'form': form})
