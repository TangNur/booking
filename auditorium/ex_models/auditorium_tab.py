from django.db import models

from auditorium.ex_models.auditorium_type_tab import AuditoriumTypeTab
from auditorium.ex_models.block_tab import BlockTab
from auditorium.ex_models.floor_tab import FloorTab


class AuditoriumTab(models.Model):
    auditorium_id = models.AutoField(primary_key=True)
    is_allowed = models.BooleanField(blank=True, null=True)
    block = models.ForeignKey(BlockTab, models.DO_NOTHING, blank=True, null=True)
    floor = models.ForeignKey(FloorTab, models.DO_NOTHING, blank=True, null=True)
    auditorium_type = models.ForeignKey(AuditoriumTypeTab, models.DO_NOTHING, blank=True, null=True)
    auditorium_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditorium_tab'
