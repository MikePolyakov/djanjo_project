from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from .models import Article, Post, Statistic, Source
from .forms import ContactForm, PostForm


# Create your views here.
def main_view(request):
    statistics = Statistic.objects.all()
    date = Article.objects.first().date
    return render(request, 'situation_report_app/index.html', context={'statistics': statistics,
                                                                       'date': date})


def articles(request):
    articles = Article.objects.order_by('-date')
    return render(request, 'situation_report_app/articles.html', context={'articles': articles})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            image = form.cleaned_data['image']
            form.save()
            return HttpResponseRedirect(reverse('app_page:index'))
        else:
            return render(request, 'situation_report_app/create.html', context={'form': form})
    else:
        form = PostForm()
        return render(request, 'situation_report_app/create.html', context={'form': form})


def posts(request):
    posts = Post.objects.all()
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
