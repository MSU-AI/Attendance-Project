from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('oldapp/', views.oldapp, name='oldapp'),
    path('', include('gsheets.urls')),
]
