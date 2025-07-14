from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', ]


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['phone', 'first_name', 'last_name', 'email', 'password', 'password2']

    def validate(self, data):
        password = data.get("password")
        password2 = data.pop("password2")
        if password != password2:
            raise serializers.ValidationError({"password": "passwords must match"})
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        user = CustomUser.objects.create_user(**validated_data)
        return user


class SigninSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, style={'input_type': 'phone'})

    def validate_phone(self, value):
        if not (value, value.isdigit()):
            raise serializers.ValidationError({"phone": "phone field is not valid"})
        return value


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    verify_token = serializers.CharField(required=True)

    def validate_phone(self, value):
        if not (value, value.isdigit()):
            raise serializers.ValidationError({"phone": "phone field is not valid"})
        return value

