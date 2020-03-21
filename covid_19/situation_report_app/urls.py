from django.urls import path
from situation_report_app import views

app_name = 'situation_report_app'

urlpatterns = [
    path('', views.StatisticListView.as_view(), name='index'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('add_article/', views.ArticleCreateView.as_view(), name='add_article'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post_detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('create_post/', views.PostCreateView.as_view(), name='create_post'),
    path('sources/', views.SourceListView.as_view(), name='sources'),
    path('contact/', views.contact, name='contact'),
    path('add_source/', views.SourceCreateView.as_view(), name='add_source'),
    path('source_news/<int:pk>/', views.SourceNewsListView.as_view(), name='source_news'),
]
