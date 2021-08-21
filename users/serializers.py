from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

# User Serializer


class UserSerializer(serializers.ModelSerializer):


  class Meta:
    model = User
    fields = ('username','email','password','first_name','last_name')
    # exclude = [
    #   'is_superuser',
    #   'is_active',
    #   'groups'
    # ]
    extra_kwargs = {'password': {'write_only': True}}

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):

  def create(self, validated_data):
    user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

    return user

  class Meta:
    model = User
    fields = "__all__"
    extra_kwargs = {'password': {'write_only': True}}

# Login Serializer


class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect Credentials")


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value