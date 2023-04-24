from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView

from auditorium.services import read_auditorium, read_auditorium_schedule, read_floor, read_block, read_auditorium_type_tab
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


class FloorView(APIView):

    def get(self, request):
        res = read_floor()

        return Response(
            {
                "floors": res
            }
        )


class BlockView(APIView):

    def get(self, request):
        res = read_block()

        return Response(
            {
                "blocks": res
            }
        )
    

class AuditoriumTypeView(APIView):

    def get(self, request):
        res = read_auditorium_type_tab()

        return Response(
            {
                "blocks": res
            }
        )
    