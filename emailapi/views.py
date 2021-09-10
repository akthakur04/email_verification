# header files
import jwt
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from rest_framework.views import APIView
from django.contrib.auth.models import User

from api import settings
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from .utils import Util


# Api view to see userlist
class UserList(APIView):
    def get(self, request):
        email1 = User.objects.all()
        serializer = UserSerializer(email1, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        # create and save user.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # send verification mail to user
        user_data = serializer.data
        users = User.objects.get(email=user_data['email'])
        tokens = AuthToken.objects.create(user)[1]
        current_site = get_current_site(request).domain
        relative_link = reverse('verify')
        absurl = 'http://' + current_site + relative_link + '?token=' + str(tokens)
        email_body = "hi " + users.username + " click the given link to verify \n" + absurl
        data = {'email_body': email_body, 'email_to': users.email, 'subject': 'verify email'}
        Util.send_email(data)

        # return API response
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": tokens,
            "message": "check your email for verification"
        })

# Verified API
class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        # TRY METHOD TO DECODE TOKEN
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'succesfully ativated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'eRROR': 'EXPIRED'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.exceptions.DecodeError as identifier:
            return Response({'email': 'succesfully ativated'}, status=status.HTTP_200_OK)




# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)