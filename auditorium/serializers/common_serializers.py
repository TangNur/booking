from rest_framework import serializers

from auditorium.ex_models.auditorium_type_tab import AuditoriumTypeTab
from auditorium.ex_models.block_tab import BlockTab
from auditorium.ex_models.booking_request_status_tab import BookingRequestStatusTab
from auditorium.ex_models.floor_tab import FloorTab
from auditorium.ex_models.group_tab import GroupTab
from auditorium.ex_models.instructor_tab import InstructorTab


class BookingRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingRequestStatusTab
        fields = ('booking_request_status_id', 'booking_request_status_code', 'booking_request_status_name')


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorTab
        fields = ('instructor_id', 'instructor_name')


class GroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField()

    class Meta:
        model = GroupTab
        fields = ('group_id', 'group_name')


class AuditoriumTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditoriumTypeTab
        fields = ('auditorium_type_id', 'auditorium_type_name', 'auditorium_type_abbreviation')


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockTab
        fields = ('block_id', 'block_name', 'block_number')


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloorTab
        fields = ('floor_id', 'floor_name', 'floor_number')
