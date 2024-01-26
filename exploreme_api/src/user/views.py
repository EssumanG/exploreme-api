from rest_framework.generics import GenericAPIView
from .serializers import RegisterUserSerializer, LoginUserSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import User
from rest_framework.views import APIView

from django.contrib.auth import authenticate


class RegisterUserView(GenericAPIView):
    serializer_class = RegisterUserSerializer 
    queryset = User.objects.all()
    permission_classes = []

    def post(self, request:Request):
        user_data=request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data

            # TODO:#send emailfunction user['email']
            return Response({
                'data': user,
                'message': f'hi {user.get('username')}, thanks for signing up',
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request:Request):
        users = self.get_queryset()
        serializer = self.serializer_class(users, many=True)
        message = {
            "msg":"lists of all users",
            "data": serializer.data
        }
        return Response(message, status=status.HTTP_200_OK)
    

# TODO: Generate OTPcodes for user verification
    
class LoginUserView(APIView):
    permission_classes = []
    serializer_class = LoginUserSerializer
    queryset = User.objects.all()
    def post(self, request:Request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        print(serializer)
        content = {
            "message": "login succesfully",
            "data": serializer.data
        }

        return Response(data=content, status=status.HTTP_200_OK) 
       




    def get(self, request:Request):
        content = {
        "user": str(request.user),
        "auth":str(request.auth),
        }
        return Response(data=content, status=status.HTTP_200_OK)

    


