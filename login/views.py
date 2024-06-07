from django.http import JsonResponse
from login.models import User
from login.serializers import UserSerializer
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
import bcrypt

# Test view
@api_view(["POST"])
def test(request):
  result = User.objects.authorize(request.COOKIES)
  if "user" in result and result["user"]:
    serializer = UserSerializer(result["user"])
    result["user"] = serializer.data
  is_verified = "is_verified" in result and result["is_verified"]
  return JsonResponse(
    {
      "test": True,
      "result": result
    },
    status = status.HTTP_200_OK if is_verified else status.HTTP_401_UNAUTHORIZED
  )


def show_all_users():
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
  data["username_lower"] = data["username"].lower()
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
  
  # Save user object and return
  user.save()
  serializer = UserSerializer(user)
  response = JsonResponse(
    {"user": serializer.data},
    status = status.HTTP_201_CREATED
  )
  response.set_cookie(
    "assoc_token",
    value = user.create_token(),
    max_age = None,
    expires = None,
    httponly = True
  )
  return response


@api_view(["GET", "POST"])
def index(request):
  if request.method == "GET":
    return show_all_users()
  elif request.method == "POST":
    return create_user(request)


@api_view(["POST"])
def log_in(request):
  data = JSONParser().parse(request)
  # Make sure required data is included
  if "username" not in data and "email" not in data:
    return JsonResponse({
      "errors": {"username": "Please include username or email."}
    })
  elif "password" not in data:
    return JsonResponse({
      "errors": {"password": "Please include a password."}
    })
  # Make sure data matches with one user
  if "username" in data:
    matched_users = User.objects.filter(
      username_lower = data["username"].lower()
    )
  elif "email" in data:
    matched_users = User.objects.filter(
      email_disambiguated = User.objects.generate_simplest_email(data["email"])
    )
  if len(matched_users) == 0:
    return JsonResponse(
      {"error": {"username": "User not found."}},
      status = status.HTTP_401_UNAUTHORIZED
    )
  elif len(matched_users) > 1:
    return JsonResponse(
      {"error": {"username": "Too many users found."}},
      status = status.HTTP_401_UNAUTHORIZED
    )
  # Return 401 response if password invalid
  user = matched_users[0]
  is_password_valid = user.check_password(
    data["password"]
  )
  if not is_password_valid:
    return JsonResponse(
      {"error": {"password": "Password invalid."}},
      status = status.HTTP_401_UNAUTHORIZED
    )
  # Return user data if password valid
  serializer = UserSerializer(user)
  response = JsonResponse(
    {"user": serializer.data},
    status = status.HTTP_200_OK
  )
  response.set_cookie(
    "assoc_token",
    value = user.create_token(),
    max_age = None,
    expires = None,
    httponly = True
  )
  return response


@api_view(["GET", "POST"])
def log_out(request):
  response = JsonResponse(
    {"logout": True},
    status = status.HTTP_200_OK
  )
  response.delete_cookie("assoc_token")
  return response
