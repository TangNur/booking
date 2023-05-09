from django.db import models

from auditorium.ex_models.auditorium_day_tab import AuditoriumDayTab
from auditorium.ex_models.group_tab import GroupTab


class AuditoriumDayGroupTab(models.Model):
    auditorium_day_group_id = models.AutoField(primary_key=True)
    auditorium_day = models.ForeignKey(AuditoriumDayTab, models.DO_NOTHING, blank=True, null=True)
    group = models.ForeignKey(GroupTab, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditorium_day_group_tab'
