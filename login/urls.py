from django.urls import path
from . import views

urlpatterns = [
  path("test", views.test),
  path("", views.index),
  path("login", views.log_in),
  path("logout", views.log_out),
  path("<int:user_id>", views.one_user),
]