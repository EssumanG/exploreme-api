from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token


class RegisterUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length =255)
    password=serializers.CharField(min_length=6, write_only=True)
    username = serializers.CharField(max_length =255)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'date_joined']

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']):
            raise ValidationError("Email already exist")
        if User.objects.filter(email=attrs['email']):
            raise ValidationError("Username already exist")
        return attrs

    def create(self , validated_data):
        print("hello")
        password = validated_data.pop("password")


        user= User.objects.create(**validated_data)
        user.set_password(password)
        print("jojo",user)
        user.save()

        Token.objects.create(user=user)
        return user
    
class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'access_token', 'refresh_token', 'username']
        

    def validate(self, attrs):
        request=self.context.get('request')
        user = authenticate(request,**attrs)
        print("user1",user)
        if not user:
            raise AuthenticationFailed("invalid credentials try again")
        user_tokens = user.tokens()


        return {
            'email': user.email,
            'username': user.get_username(),
            'refresh_token': user_tokens.get("refresh"),
            'access_token': user_tokens.get("access")
        }
    


