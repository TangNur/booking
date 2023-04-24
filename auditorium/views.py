from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from auditorium.services import read_auditorium, read_auditorium_schedule
from auditorium.utils import empty_to_none, validate_date_psql


class AuditoriumView(ViewSet):

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
