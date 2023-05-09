import datetime

from django.db import connection


def call_an_sp(method, args, has_cursor=True, session_user_id=None):
    c = connection.cursor()
    if session_user_id:
        c.execute('set session "myapp.user_id"=%s' % session_user_id)
    if has_cursor:
        c.execute("BEGIN")
    c.callproc(method, args)
    return fn_generic(c, has_cursor)


def fn_generic(cursor, has_cursor=True):
    if has_cursor:
        msg = cursor.fetchone()[0]
        cursor.execute('FETCH ALL IN "%s"' % msg)
    rows = cursor.fetchall()
    desc = [item[0] for item in cursor.cursor.description]
    thing = [dict(zip(desc, item)) for item in rows]
    cursor.close()
    return thing


def empty_to_none(s):
    if s is not None:
        if isinstance(s, list):
            if not s:
                return None
        if isinstance(s, str):
            if len(s.strip()) == 0:
                return None
            else:
                return s.strip()
    return s


def validate_date_psql(date_text, is_null_available=False):
    try:
        if not is_null_available and not date_text:
            raise Exception('Введите дату!')
        if date_text:
            converted = datetime.datetime.strptime(date_text, '%d.%m.%Y')
            return converted.strftime('%Y-%m-%d')
        else:
            return None
    except ValueError:
        raise ValueError("Неверный формат даты. Введите DD.MM.YYYY")


def get_secret_password():
    return 'dki#ds%$'
