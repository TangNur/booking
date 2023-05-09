from django.db import models

from auditorium.ex_models.course_tab import CourseTab
from auditorium.ex_models.speciality_tab import SpecialityTab


class GroupTab(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_year = models.IntegerField(blank=True, null=True)
    group_number = models.CharField(max_length=20, blank=True, null=True)
    speciality = models.ForeignKey(SpecialityTab, models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey(CourseTab, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_tab'
