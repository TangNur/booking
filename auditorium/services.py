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


def read_auditorium_type_tab():
    res = call_an_sp('public.read_auditorium_type_tab', [], has_cursor=False)[0]['read_auditorium_type_tab']

    if res is None:
        return res

    res = json.loads(res)

    return res
