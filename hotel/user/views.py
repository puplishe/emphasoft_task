from rest_framework import generics
from .serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    