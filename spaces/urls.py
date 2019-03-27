from django.urls import path
from . import views

app_name = 'spaces'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.post_new, name='post_new'),
]

