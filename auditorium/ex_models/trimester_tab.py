from django.db import models


class TrimesterTab(models.Model):
    trimester_id = models.AutoField(primary_key=True)
    trimester_name = models.CharField(max_length=100, blank=True, null=True)
    trimester_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trimester_tab'
