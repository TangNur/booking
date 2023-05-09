from django.db import models


class FloorTab(models.Model):
    floor_id = models.AutoField(primary_key=True)
    floor_name = models.CharField(max_length=100, blank=True, null=True)
    floor_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'floor_tab'
