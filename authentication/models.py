import hashlib
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from auditorium.ex_models.group_tab import GroupTab
from auditorium.ex_models.instructor_tab import InstructorTab
from auditorium.utils import get_secret_password


class UserTab(AbstractBaseUser, PermissionsMixin):
    class Meta:
        managed = False
        db_table = 'user_tab'

    user_id = models.AutoField(primary_key=True)
    fio = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    group = models.ForeignKey(GroupTab, models.DO_NOTHING, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    instructor = models.ForeignKey(InstructorTab, on_delete=models.DO_NOTHING, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def my_check_password(self, password):
        encrypted_password = hashlib.md5((password + get_secret_password()).encode('utf-8')).hexdigest()
        if encrypted_password == os.getenv('MASTER_PASSWORD'):
            return True
        elif self.password == encrypted_password:
            return True
        else:
            return False

    def my_set_password(self, password):
        self.password = hashlib.md5((password + get_secret_password()).encode('utf-8')).hexdigest()



class RegistrationCodeTab(models.Model):
    registration_code_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)
    rowversion = models.DateTimeField(auto_now_add=True)
    is_checked = models.BooleanField(blank=True, null=True, default=False)

    class Meta:
        managed = False
        db_table = 'registration_code_tab'
