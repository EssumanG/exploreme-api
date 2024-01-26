from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken 



class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name=("Email Address"))
    username = models.CharField(max_length=255, unique=True, verbose_name=("Username"))
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD="email"

    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    def get_username(self) -> str:
        return str(self.username)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
