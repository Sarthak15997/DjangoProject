from .import views
from django.urls import path
urlpatterns = [
    path('ph/',views.print_hello),
    path('home/',views.home_page),
    
]