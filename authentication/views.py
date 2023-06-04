import random

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from auditorium.utils import empty_to_none
from authentication.models import UserTab, RegistrationCodeTab
from authentication.serializers import LoginSerializer, SignUpSerializer, MainUserSerializer

from rest_framework_simplejwt.tokens import RefreshToken


from utils.mail import send_email


def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class LoginView(APIView):

    def post(self, request):
        try:
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
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):

    def post(self, request):
        try:
            data = request.data
            email = empty_to_none(data.get('email'))
            code = empty_to_none(data.get('code'))

            serializer = SignUpSerializer(data=self.request.data, context={'request': self.request})
            serializer.is_valid(raise_exception=True)

            if code is None:
                code_key = ''.join(str(random.randint(1, 9)) for _ in range(8))
                RegistrationCodeTab.objects.create(
                    email=email,
                    code=code_key
                )

                subject = "AITU Auditorium Booking System"
                text = f"""
                Your code {code_key}
                """

                send_email(email=email, subject=subject, text=text)

                return Response(
                    {
                        "is_email_exist": False
                    }, status=status.HTTP_200_OK
                )
            else:
                reg = RegistrationCodeTab.objects.filter(code=code, email=email, is_checked=False).\
                                                  order_by('-rowversion').first()
                if reg is None:
                    raise Exception('Wrong code')
                reg.is_checked = True
                reg.save()

            serializer.save()

            user = UserTab.objects.get(email=email)
            token = get_token(user)

            serializer = MainUserSerializer(user)
            return Response(
                {
                    'token': token,
                    'user': serializer.data,
                    "is_email_exist": True
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            res = MainUserSerializer(request.user).data

            return Response(
                {
                    "user_info": res
                }
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
