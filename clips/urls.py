from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("<path:path>", views.clip, name='clip'),
]