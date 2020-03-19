from django.urls import path
from situation_report_app import views

app_name = 'situation_report_app'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('articles/', views.articles, name='articles'),
    path('add_article/', views.add_article, name='add_article'),
    path('oldnews/', views.oldnews, name='oldnews'),
    path('posts/', views.posts, name='posts'),
    path('create/', views.create, name='create'),
    path('post/<int:id>/', views.post, name='post'),
    path('sources/', views.sources, name='sources'),
    path('contact/', views.contact, name='contact'),
]
