from django.urls import path
from . import views

urlpatterns = [
  path("test", views.test),
  path("user", views.index),
  path("login", views.login),
]