from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
  def generate_simplest_email(self, email):
    name, domain = email.split("@")
    short_name = ""
    for char in name:
      if char == "+":
        break
      if char != ".":
        short_name += char.lower()
    return f"{short_name.lower()}@{domain.lower()}"

  def basic_validator(self, user):
    errors = {}
    if len(user.username) < 2:
      errors["username"] = "Username must be at least 2 characters."
    if len(User.objects.filter(username = user.username)):
      errors["username"] = "This username is taken."
    if(len(user.password) < 8):
      errors["password"] = "Password must be at least 8 characters."
    if user.email and len(User.objects.filter(email_disambiguated = user.email_disambiguated)):
      errors["email"] = "There is already a user registered with this email address."
    return errors



class User(models.Model):
  username = models.CharField(
    max_length = 31
  )
  email = models.EmailField(
    blank = True
  )
  email_disambiguated = models.EmailField(
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
  objects = UserManager()

  def __str__(self):
    return f"{self.username} ({self.email})" if self.email else self.username

  def check_password(self, password_input):
    is_valid = bcrypt.checkpw(
      password_input.encode(),
      self.password.encode()
    )
    return is_valid