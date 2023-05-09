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


def read_floor():
    res = call_an_sp('public.read_floor', [], has_cursor=False)[0]['read_floor']

    if res is None:
        return res

    res = json.loads(res)

    return res


def read_block():
    res = call_an_sp('public.read_block', [], has_cursor=False)[0]['read_block']

    if res is None:
        return res

    res = json.loads(res)

    return res


def read_auditorium_type():
    res = call_an_sp('public.read_auditorium_type', [], has_cursor=False)[0]['read_auditorium_type']

    if res is None:
        return res

    res = json.loads(res)

    return res


def read_group():
    res = call_an_sp('public.read_group', [], has_cursor=False)[0]['read_group']

    if res is None:
        return res

    res = json.loads(res)

    return res


def read_instructor():
    res = call_an_sp('public.read_instructor', [], has_cursor=False)[0]['read_instructor']

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


def approve_request(user_id, booking_request_id):
    call_an_sp('approve_request', [user_id, booking_request_id], has_cursor=False)

    return True
