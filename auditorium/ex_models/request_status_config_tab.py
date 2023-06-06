from django.db import models


class RequestStatusConfigTab(models.Model):
    request_status_config_id = models.AutoField(primary_key=True)
    request_status_config_code = models.CharField(max_length=255, blank=True, null=True)
    request_status_config_name = models.CharField(max_length=255, blank=True, null=True)
    is_chosen = models.BooleanField(unique=True)

    class Meta:
        managed = False
        db_table = 'request_status_config_tab'
