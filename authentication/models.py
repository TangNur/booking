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
    fio = models.CharField(max_length=512)
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
