from django.db import models


class SpecialityTab(models.Model):
    speciality_id = models.AutoField(primary_key=True)
    speciality_name = models.CharField(max_length=100, blank=True, null=True)
    speciality_abbreviation = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'speciality_tab'
