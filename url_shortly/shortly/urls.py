from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_short_url, name='create_short_url'),
    path('<str:short_code>/', views.redirect_to_url, name='redirect_to_url'),
]
