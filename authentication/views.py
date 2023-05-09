from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from auditorium.utils import empty_to_none
from authentication.models import UserTab
from authentication.serializers import LoginSerializer, SignUpSerializer, MainUserSerializer

from rest_framework_simplejwt.tokens import RefreshToken


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        email = empty_to_none(data.get('email'))
        password = empty_to_none(data.get('password'))

        if email is None or password is None:
            raise Exception("Enter credentials")

        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_token(user)

        serializer = MainUserSerializer(user)
        return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        email = empty_to_none(data.get('email'))

        serializer = SignUpSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = UserTab.objects.get(email=email)
        token = get_token(user)

        serializer = MainUserSerializer(user)
        return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
