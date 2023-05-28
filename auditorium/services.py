import json

from auditorium.utils import call_an_sp


def read_auditorium(floor_id, block_id):
    res = call_an_sp('public.read_auditorium', [floor_id, block_id], has_cursor=False)[0]['read_auditorium']

    if res is None:
        return res

    res = json.loads(res)

    return res


def read_auditorium_schedule(auditorium_id, day):
    res = call_an_sp(
        'public.read_auditorium_schedule', [auditorium_id, day], has_cursor=False
    )[0]['read_auditorium_schedule']

    if res is None:
        return res

    res = json.loads(res)

    return res


def request_booking_auditorium(user_id, auditorium_id, reason, datetime_from, datetime_to):
    call_an_sp('request_booking_auditorium', [user_id, auditorium_id, reason, datetime_from, datetime_to],
               has_cursor=False)

    return True


def read_booking_request_for_user(user_id):
    res = call_an_sp('public.read_booking_request_for_user', [user_id],
                     has_cursor=False)[0]['read_booking_request_for_user']

    if res is None:
        return res

    res = json.loads(res)

    return res


def approve_request(user_id, booking_request_id, booking_request_status_id, reason_for_refuse):
    call_an_sp('approve_request', [user_id, booking_request_id, booking_request_status_id, reason_for_refuse],
               has_cursor=False)

    return True

