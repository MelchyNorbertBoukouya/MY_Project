from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('country/<str:code>/', views.country_detail, name='country_detail'),
]
