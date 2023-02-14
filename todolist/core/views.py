from django.contrib.auth import login, logout
from rest_framework import generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from core.models import User, TgUser

from core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer, \
    TgUserSerializer, TgUserConnectSerializer, TgUserDeleteSerializer


class SignUpView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        login(request=self.request, user=serializer.save())


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    # authentication_classes = [TgUserAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        return self.request.user


class TgUserConnectView(generics.CreateAPIView):
    serializer_class = TgUserConnectSerializer


class TgUserVerifyView(generics.UpdateAPIView):
    queryset = TgUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TgUserSerializer

    def get_object(self):
        obj = get_object_or_404(self.queryset, verification_code=self.request.data.get('verification_code'))
        return obj


class TgUserDeleteView(generics.DestroyAPIView):
    queryset = TgUser.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TgUserDeleteSerializer
    lookup_field = 'tg_user'
