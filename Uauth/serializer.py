from django.contrib.auth import authenticate
from rest_framework import serializers
from . import *
from .models import customUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    email = serializers.EmailField(required=False)
    class Meta:
        model = customUser
        fields = ('username', 'password', 'email')
        authentication_classes = []
    def create(self, validated_data):
        user = customUser.objects.create_user(
            validated_data['username'],
            validated_data['password'],
            email=validated_data.get('email', None)
        )
        if not user:
            raise serializers.ValidationError("error while registering user.")
        return user
    



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'},write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username is None or password is None:
            raise serializers.ValidationError("A username and password are required to login.")
       
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        data['user'] = user
        return data

