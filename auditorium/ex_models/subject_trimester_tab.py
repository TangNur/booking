from django.db import models

from auditorium.ex_models.instructor_tab import InstructorTab
from auditorium.ex_models.subject_tab import SubjectTab
from auditorium.ex_models.trimester_tab import TrimesterTab


class SubjectTrimesterTab(models.Model):
    subject_trimester_id = models.AutoField(primary_key=True)
    subject_trimester_year = models.IntegerField(blank=True, null=True)
    trimester = models.ForeignKey(TrimesterTab, models.DO_NOTHING, blank=True, null=True)
    subject = models.ForeignKey(SubjectTab, models.DO_NOTHING, blank=True, null=True)
    instructor = models.ForeignKey(InstructorTab, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_trimester_tab'
