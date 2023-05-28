from django.db import transaction, DatabaseError, models
from django.db.models import F, Value
from django.db.models.functions import Concat

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from auditorium.ex_models.auditorium_type_tab import AuditoriumTypeTab
from auditorium.ex_models.block_tab import BlockTab
from auditorium.ex_models.booking_request_status_tab import BookingRequestStatusTab
from auditorium.ex_models.floor_tab import FloorTab
from auditorium.ex_models.group_tab import GroupTab
from auditorium.ex_models.instructor_tab import InstructorTab

from auditorium.serializers.common_serializers import BookingRequestStatusSerializer, InstructorSerializer, \
    GroupSerializer, AuditoriumTypeSerializer, BlockSerializer, FloorSerializer

from auditorium.services import read_auditorium, read_auditorium_schedule, request_booking_auditorium, \
    read_booking_request_for_user, approve_request

from auditorium.utils import empty_to_none, validate_date_psql


class AuditoriumView(ViewSet):
    permission_classes = (IsAuthenticated,)

    def read(self, request):
        floor_id = empty_to_none(request.query_params.get('floor_id'))
        block_id = empty_to_none(request.query_params.get('block_id'))

        res = read_auditorium(floor_id=floor_id, block_id=block_id)

        return Response(
            {
                "auditoriums": res
            }
        )

    def read_schedule(self, request, auditorium_id):
        day = validate_date_psql(
            empty_to_none(request.query_params.get('day')),
            is_null_available=True
        )

        res = read_auditorium_schedule(auditorium_id=auditorium_id, day=day)

        return Response(
            {
                "auditorium_schedule": res
            }
        )

    def request(self, request, auditorium_id):
        try:
            with transaction.atomic():
                data = request.data

                user_id = request.user.user_id
                reason = empty_to_none(data.get('reason'))
                datetime_from = empty_to_none(data.get('datetime_from'))
                datetime_to = empty_to_none(data.get('datetime_to'))

                request_booking_auditorium(
                    user_id=user_id,
                    auditorium_id=auditorium_id,
                    reason=reason,
                    datetime_from=datetime_from,
                    datetime_to=datetime_to
                )

                day = validate_date_psql(
                    empty_to_none(request.query_params.get('day')),
                    is_null_available=True
                )

                res = read_auditorium_schedule(auditorium_id=auditorium_id, day=day)

                return Response(
                    {
                        "auditorium_schedule": res
                    }
                )
        except DatabaseError as e:
            error = str(e)
            error = error[error.find("{") + 1:error.find("}")]
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def approve(self, request):
        try:
            with transaction.atomic():
                data = request.data

                user_id = request.user.user_id
                booking_request_id = empty_to_none(data.get('booking_request_id'))
                booking_request_status_id = empty_to_none(data.get('booking_request_status_id'))

                approve_request(
                    user_id=user_id,
                    booking_request_id=booking_request_id,
                    booking_request_status_id=booking_request_status_id
                )

                res = read_booking_request_for_user(user_id=request.user.user_id)

                return Response(
                    {
                        "requests": res
                    }
                )
        except DatabaseError as e:
            error = str(e)
            error = error[error.find("{") + 1:error.find("}")]
            return Response(
                {
                    "error": error
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def read_reqeust_for_user(self, request):
        res = read_booking_request_for_user(user_id=request.user.user_id)

        return Response(
            {
                "requests": res
            }
        )


class FloorView(APIView):

    def get(self, request):
        queryset = FloorTab.objects.order_by('floor_number')
        res = FloorSerializer(queryset, many=True).data

        return Response(
            {
                "floors": res
            }
        )


class BlockView(APIView):

    def get(self, request):
        queryset = BlockTab.objects.order_by('block_number')
        res = BlockSerializer(queryset, many=True).data

        return Response(
            {
                "blocks": res
            }
        )
    

class AuditoriumTypeView(APIView):

    def get(self, request):
        queryset = AuditoriumTypeTab.objects.order_by('auditorium_type_abbreviation')
        res = AuditoriumTypeSerializer(queryset, many=True).data

        return Response(
            {
                "auditorium_types": res
            }
        )


class GroupView(APIView):

    def get(self, request):
        queryset = GroupTab.objects.order_by('group_year', 'course_id').values('group_id').annotate(
            group_name=Concat(
                'speciality__speciality_abbreviation',
                Value('-'),
                F('group_year'),
                F('group_number'),
                output_field=models.CharField()
            )
        ).values('group_id', 'group_name')
        res = GroupSerializer(queryset, many=True).data

        return Response(
            {
                "groups": res
            }
        )


class InstructorView(APIView):

    def get(self, request):
        queryset = InstructorTab.objects.filter(is_active=True).order_by('instructor_name')
        res = InstructorSerializer(queryset, many=True).data

        return Response(
            {
                "instructors": res
            }
        )


class BookingRequestStatusView(APIView):

    def get(self, request):
        queryset = BookingRequestStatusTab.objects.filter(is_active=True).order_by('booking_request_status_name')
        res = BookingRequestStatusSerializer(queryset, many=True).data

        return Response(
            {
                "booking_request_status_ids": res
            }
        )
