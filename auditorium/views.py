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
from auditorium.ex_models.booking_request_tab import BookingRequestTab
from auditorium.ex_models.floor_tab import FloorTab
from auditorium.ex_models.group_tab import GroupTab
from auditorium.ex_models.instructor_tab import InstructorTab
from auditorium.ex_models.request_status_config_tab import RequestStatusConfigTab

from auditorium.serializers.common_serializers import BookingRequestStatusSerializer, InstructorSerializer, \
    GroupSerializer, AuditoriumTypeSerializer, BlockSerializer, FloorSerializer, RequestStatusConfigSerializer

from auditorium.services import read_auditorium, read_auditorium_schedule, request_booking_auditorium, \
    read_booking_request_for_user, approve_request

from auditorium.utils import empty_to_none, validate_date_psql, call_an_sp
from authentication.models import UserTab
from utils.mail import send_email


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
                reason_for_refuse = empty_to_none(data.get('reason_for_refuse'))

                approve_request(
                    user_id=user_id,
                    booking_request_id=booking_request_id,
                    booking_request_status_id=booking_request_status_id,
                    reason_for_refuse=reason_for_refuse
                )

                booking_request_status = BookingRequestStatusTab.objects.get(
                    booking_request_status_id=booking_request_status_id
                )

                booking_request = BookingRequestTab.objects.get(booking_request_id=booking_request_id)

                receiving_user = UserTab.objects.get(user_id=booking_request.user_id)

                if receiving_user.is_staff:
                    user_fio = InstructorTab.objects.get(instructor_id=receiving_user.instructor_id).instructor_name
                else:
                    user_fio = receiving_user.fio

                auditorium_name = call_an_sp(
                    'get_auditorium_name', [booking_request.auditorium_id], has_cursor=False
                )[0]['get_auditorium_name']

                if reason_for_refuse is not None:
                    reason_for_refuse = 'Reason: ' + reason_for_refuse

                if booking_request_status.booking_request_status_code == 'ACCEPTED':
                    reason_for_refuse = ""

                subject = "AITU Auditorium Booking System"
                text = f"""
                Dear {user_fio}!

                Your request to book an auditorium {auditorium_name} 
                for this {booking_request.datetime_from} - {booking_request.datetime_to} time period 
                was {booking_request_status.booking_request_status_code}
                
                {reason_for_refuse}
                """

                send_email(email=receiving_user.email, subject=subject, text=text)

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


class RequestStatusConfigView(ViewSet):
    permission_classes = (IsAuthenticated,)

    def read_all(self, request):
        queryset = RequestStatusConfigTab.objects.order_by('request_status_config_code')
        res = RequestStatusConfigSerializer(queryset, many=True).data

        return Response(
            {
                "request_status_configs": res
            }
        )

    def change(self, request):
        data = request.data

        request_status_config_id = data.get('request_status_config_id')

        user = UserTab.objects.get(user_id=request.user.user_id)
        if not user.is_superuser:
            raise Exception('You do not have permission for this action')

        new_chosen = RequestStatusConfigTab.objects.filter(request_status_config_id=request_status_config_id).first()
        if new_chosen is None:
            raise Exception('This status does not exist')

        old_chosen = RequestStatusConfigTab.objects.get(is_chosen=True)
        old_chosen.is_chosen = False
        old_chosen.save()

        new_chosen.is_chosen = True
        new_chosen.save()

        return self.read_all(request)
