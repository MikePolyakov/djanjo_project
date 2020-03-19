from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from urllib.parse import urlparse
import datetime
from .models import Article, Post, Statistic, Source
from .forms import ContactForm, PostForm, NewsForm
from situation_report_app.update import update


# Create your views here.
def main_view(request):
    statistics = Statistic.objects.all()
    print(len(statistics))
    if len(statistics) > 0:
        last_date = Statistic.objects.first().date
    else:
        last_date = datetime.date.today()
    if request.method == 'GET':
        update()
    return render(request, 'situation_report_app/index.html', context={'statistics': statistics,
                                                                       'show_date': last_date})


def articles(request):
    articles = Article.objects.order_by('-date')[:10]
    return render(request, 'situation_report_app/articles.html', context={'articles': articles})


def oldnews(request):
    oldnews = Article.objects.order_by('-date')[10:]
    return render(request, 'situation_report_app/oldnews.html', context={'oldnews': oldnews})


def add_article(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            url = form.cleaned_data['url']
            date = form.cleaned_data['date']
            source = form.cleaned_data['source']
            if not Article.objects.filter(url=url).exists():
                url_source = urlparse(url).netloc
                if not Source.objects.filter(url=url_source).exists():
                    Source.objects.create(name=source, url=url_source)
                Article.objects.create(date=date,
                                       name=name,
                                       source=Source.objects.filter(url=url_source).first(),
                                       url=url)
            return HttpResponseRedirect(reverse('app_page:articles'))
        else:
            return render(request, 'situation_report_app/add_article.html', context={'form': form})
    else:
        form = NewsForm()
        return render(request, 'situation_report_app/add_article.html', context={'form': form})


def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            Post.objects.create(name=name,
                                text=text
                                )
            return HttpResponseRedirect(reverse('app_page:posts'))
        else:
            return render(request, 'situation_report_app/create.html', context={'form': form})
    else:
        form = PostForm()
        return render(request, 'situation_report_app/create.html', context={'form': form})


def posts(request):
    posts = Post.objects.all()[:10]
    return render(request, 'situation_report_app/posts.html', context={'posts': posts})


def sources(request):
    sources = Source.objects.all()
    return render(request, 'situation_report_app/sources.html', context={'sources': sources})


def post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'situation_report_app/post.html', context={'post': post})


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
            return HttpResponseRedirect(reverse('app_page:index'))
        else:
            return render(request, 'situation_report_app/contact.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'situation_report_app/contact.html', context={'form': form})
