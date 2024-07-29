from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from oauth.models import UserModel


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])

        try:
            user = UserModel.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("User with this email already exists.")

        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")
