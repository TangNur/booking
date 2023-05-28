from django.db import models


class BookingRequestStatusTab(models.Model):
    booking_request_status_id = models.AutoField(primary_key=True)
    booking_request_status_name = models.CharField(max_length=255)
    booking_request_status_code = models.CharField(max_length=255)
    is_active = models.BooleanField()
    rowversion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'booking_request_status_tab'
