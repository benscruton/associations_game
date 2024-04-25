from django.db import models

# Create your models here.
class User(models.Model):
  username = models.CharField(
    max_length = 31
  )
  email = models.EmailField(
    blank = True
  )
  password = models.TextField()
  name = models.TextField(
    blank = True
  )
  created_at = models.DateTimeField(
    auto_now_add = True
  )
  updated_at = models.DateTimeField(
    auto_now = True
  )

  def __str__(self):
    return f"{self.username} ({self.email})" if self.email else self.username