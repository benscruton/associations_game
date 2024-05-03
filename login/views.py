from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from login.models import User
from login.serializers import UserSerializer
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import bcrypt

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

