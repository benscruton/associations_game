from django.shortcuts import render
from django.http import JsonResponse
from login.models import User
from login.serializers import UserSerializer
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import bcrypt
import os

# Create your views here.
def test(request):
  return JsonResponse({
    "test": True
  })

def show_all_users(request):
  users = User.objects.all()
  serializer = UserSerializer(
    users,
    many = True
  )
  return JsonResponse(
    serializer.data,
    safe = False
  )

def create_user(request):
  data = JSONParser().parse(request)
  if "email" in data:
    data["email_disambiguated"] = User.objects.generate_simplest_email(data["email"])

  # Create and validate ORM object
  user = User(**data)
  errors = User.objects.basic_validator(user)
  if errors:
    return JsonResponse(
      {"errors": errors},
      status = status.HTTP_400_BAD_REQUEST
    )

  # Hash password before proceeding
  hashed_pw = bcrypt.hashpw(
    user.password.encode(),
    bcrypt.gensalt()
  ).decode()
  user.password = hashed_pw
  del data["password"]
  
  user.save()
  serializer = UserSerializer(user)
  return JsonResponse(
    {"user": serializer.data},
    status = status.HTTP_201_CREATED
  )

@api_view(["GET", "POST"])
def index(request):
  if request.method == "GET":
    return show_all_users(request)
  elif request.method == "POST":
    return create_user(request)

@api_view(["POST"])
def login(request):
  data = JSONParser().parse(request)
  # Make sure required data is included
  if ("username" not in data and "email" not in data) or "password" not in data:
    return JsonResponse(
      {"error": "Please include a password, as well as either a username or email."}
    )
  # Make sure data matches with one user
  if "username" in data:
    matched_users = User.objects.filter(
      username = data["username"]
    )
  elif "email" in data:
    matched_users = User.objects.filter(
      email_disambiguated = User.objects.generate_simplest_email(data["email"])
    )
  if len(matched_users) == 0:
    return JsonResponse(
      {"error": "User not found."},
      status = status.HTTP_404_NOT_FOUND
    )
  elif len(matched_users) > 1:
    return JsonResponse(
      {"error": "Too many users found."},
      status = status.HTTP_400_BAD_REQUEST
    )
  # Return 401 response if password invalid
  user = matched_users[0]
  is_password_valid = user.check_password(
    data["password"]
  )
  if not is_password_valid:
    return JsonResponse(
      {"error": "Password invalid."},
      status = status.HTTP_401_UNAUTHORIZED
    )
  # Return user data if password valid
  serializer = UserSerializer(user)
  return JsonResponse(
    {"user": serializer.data},
    status = status.HTTP_200_OK
  )
  
  
@api_view(["GET"])
def test_env(request):
  return JsonResponse(
    {"test": os.getenv("TEST")},
    status = status.HTTP_200_OK
  )