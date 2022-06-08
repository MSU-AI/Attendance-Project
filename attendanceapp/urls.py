from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app/', views.app, name='app'),
    path('oldapp/', views.oldapp, name='oldapp'),
    path('sync/', views.sync, name='sync'),
    path('register/<slug:groupid>', views.user_register, name='demoreg'),
]
