import random

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

            serializer = SignUpSerializer(data=self.request.data, context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = UserTab.objects.get(email=email)
            token = get_token(user)

            serializer = MainUserSerializer(user)
            return Response({'token': token, 'user': serializer.data}, status=status.HTTP_200_OK)
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


# class PasswordResetView(APIView):
#
#     def post(self, request):
#         try:
#             data = request.data
#             email = data.get('email')
#
#             user = UserTab.objects.filter(email=email).first()
#             if not user:
#                 raise Exception('Access denied: not existing email')
#
#             # if user.last_reset_password_date:
#             #     delta = datetime.now() - user.last_reset_password_date
#             #     if divmod(delta.seconds, 60)[0] < 2:
#             #         left = round(2 - divmod(delta.seconds, 60)[0] - 1)
#             #         seconds = round(60 - (delta.seconds % 60))
#             #
#             #         raise Exception(f'Сбрасывать повторно пароль можно только через 2 минуты. '
#             #                         f'Осталось {left}:{seconds}')
#
#             user_new_password = ''.join(str(random.randint(0, 9)) for _ in range(8))
#             user.my_set_password(user_new_password)
#             # user.reset_password_cnt = nvl(user.reset_password_cnt, 0) + 1
#             # user.last_reset_password_date = datetime.now()
#             user.save()
#
#             subject = "Reset the password of the AITU Auditorium Booking system"
#             text = f"""
#             Уважаемый (-ая), {user.fio}!
#
#             Направляем данные для входа в систему Smart Remont
#             Ваш новый пароль: {user_new_password}
#
#             С уважением,
#             Команда Smart Remont
#
#                     """
#
#             send_email(email=email, subject=subject, text=text)
#             return Response(
#                 {
#                     "status": True
#                 }
#             )
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
