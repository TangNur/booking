from django.db import models


class AuditoriumTypeTab(models.Model):
    auditorium_type_id = models.AutoField(primary_key=True)
    auditorium_type_name = models.CharField(max_length=100, blank=True, null=True)
    auditorium_type_abbreviation = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditorium_type_tab'
