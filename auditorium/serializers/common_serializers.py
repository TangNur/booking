from rest_framework import serializers

from auditorium.ex_models.booking_request_status_tab import BookingRequestStatusTab


class BookingRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequestStatusTab
        fields = ('booking_request_status_id', 'booking_request_status_code', 'booking_request_status_name')
