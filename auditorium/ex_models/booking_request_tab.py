from django.db import models

from auditorium.ex_models.auditorium_tab import AuditoriumTab
from auditorium.ex_models.booking_request_status_tab import BookingRequestStatusTab
from authentication.models import UserTab


class BookingRequestTab(models.Model):
    booking_request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserTab, models.DO_NOTHING)
    reason = models.TextField()
    datetime_from = models.DateTimeField()
    datetime_to = models.DateTimeField()
    auditorium = models.ForeignKey(AuditoriumTab, models.DO_NOTHING)
    booking_request_status = models.ForeignKey(BookingRequestStatusTab, models.DO_NOTHING)
    rowversion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'booking_request_tab'
