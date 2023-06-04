import hashlib

from django.core.validators import EmailValidator
from rest_framework import serializers

from auditorium.ex_models.instructor_tab import InstructorTab
from auditorium.utils import get_secret_password, call_an_sp, empty_to_none
from authentication.models import UserTab


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(label='email', write_only=True)
    password = serializers.CharField(label='password', style={'input_type': 'password'}, trim_whitespace=True,
                                     write_only=True)
    is_staff = serializers.BooleanField(label='is_staff', write_only=True)
    fio = serializers.CharField(label='fio', write_only=True, required=False, allow_null=True)
    group_id = serializers.IntegerField(label='group_id', write_only=True, required=False, allow_null=True)
    instructor_id = serializers.IntegerField(label='instructor_id', write_only=True, required=False, allow_null=True)

    class Meta:
        model = UserTab
        fields = ('email', 'password', 'group_id', 'is_staff', 'fio', 'instructor_id')

    def create(self, validated_data):
        return UserTab.objects.create(**validated_data)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        is_staff = attrs.get('is_staff')
        group_id = empty_to_none(attrs.get('group_id'))
        instructor_id = empty_to_none(attrs.get('instructor_id'))

        if is_staff is True:
            if instructor_id is None:
                raise Exception("Choose instructor")
            instructor = UserTab.objects.filter(instructor_id=instructor_id, is_active=True).first()
            if instructor is not None:
                raise Exception("This instructor has already been linked to another account")
        else:
            if group_id is None:
                raise Exception("Choose group")

        if email and password:
            validator = EmailValidator()
            try:
                validator(email)
            except Exception:
                raise Exception('Invalid email address')

            domain = email.split('@')[1]

            if domain != 'astanait.edu.kz':
                raise Exception("You don't have permissions for this module with this email domain")

            user = UserTab.objects.filter(email=email).first()
            if user:
                raise Exception('Access denied: user exist')
        else:
            raise Exception('Both "email" and "password" are required.')

        attrs['password'] = hashlib.md5((password + get_secret_password()).encode('utf-8')).hexdigest()

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label='Email', write_only=True)
    password = serializers.CharField(label='Password', style={'input_type': 'password'}, trim_whitespace=True,
                                     write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = UserTab.objects.filter(email=email).first()

        if user is None:
            raise Exception('Access denied: not existing email')

        if user.is_active == 0:
            raise Exception('The user is blocked')

        if not user.my_check_password(password):
            raise Exception('Access denied: wrong password')

        attrs['user'] = user
        return attrs


class MainUserSerializer(serializers.ModelSerializer):
    group_name = serializers.SerializerMethodField()
    fio = serializers.SerializerMethodField()

    class Meta:
        model = UserTab
        fields = ('user_id', 'email', 'fio', 'group_name', 'is_superuser')

    def get_group_name(self, obj):
        return call_an_sp('get_group_name', [obj.user_id], has_cursor=False)[0]['get_group_name']

    def get_fio(self, obj):
        if obj.is_staff:
            instructor = InstructorTab.objects.get(instructor_id=obj.instructor_id)
            return instructor.instructor_name

        return obj.fio
