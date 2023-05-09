from django.db import models


class BlockTab(models.Model):
    block_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=100, blank=True, null=True)
    block_number = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'block_tab'
