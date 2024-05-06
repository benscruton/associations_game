from django.urls import path
from . import views

urlpatterns = [
  path("test", views.test),
  path("envtest", views.test_env),
  path("user", views.index),
  path("login", views.login),
]