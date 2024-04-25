from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from login.serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
def test(request):
  return JsonResponse({
    "test": True
  })

@csrf_exempt
def create(request):
  if(request.method != "POST"):
    return JsonResponse({
      "error": "Must be a POST request"
    })
  data = JSONParser().parse(request)
  serializer = UserSerializer(data = data)
  return JsonResponse({
    "isValid": serializer.is_valid(),
    "data": data
  })