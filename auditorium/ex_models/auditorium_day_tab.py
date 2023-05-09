from django.db import models

from auditorium.ex_models.auditorium_tab import AuditoriumTab
from auditorium.ex_models.subject_trimester_tab import SubjectTrimesterTab


class AuditoriumDayTab(models.Model):
    auditorium_day_id = models.AutoField(primary_key=True)
    auditorium_day_date_begin = models.DateTimeField(blank=True, null=True)
    auditorium = models.ForeignKey(AuditoriumTab, models.DO_NOTHING, blank=True, null=True)
    subject_trimester = models.ForeignKey(SubjectTrimesterTab, models.DO_NOTHING, blank=True, null=True)
    auditorium_day_date_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditorium_day_tab'
