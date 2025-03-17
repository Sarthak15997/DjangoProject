from .import views
from django.urls import path
urlpatterns = [
    path('ph/',views.print_hello),
    path('home/',views.home_page),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('users/', views.get_all_users, name='get_all_users'),
    path('users/<str:email>/', views.get_user_by_email, name='get_user_by_email'),
    path('users/update/<str:email>/', views.update_user, name='update_user'),
    path('users/delete/<str:email>/', views.delete_user, name='delete_user'),
]