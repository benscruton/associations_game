from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      "id",
      "username",
      "email",
      "email_disambiguated",
      "name",
      "created_at",
      "updated_at"
    ]
