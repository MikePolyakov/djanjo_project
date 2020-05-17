from django.urls import path
from users_app import views
from django.contrib.auth.views import LogoutView

app_name = 'users_app'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path('pass_change/', views.PasswordResetByUser.as_view(), name='pass_change'),
    path('profile/<int:pk>/', views.UserDetailView.as_view(), name='profile'),
    path('updatetoken/', views.update_user_token, name='update_token'),
]
