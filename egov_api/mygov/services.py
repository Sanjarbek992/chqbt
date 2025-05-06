from .api import get_access_token, fetch_teacher_data
from .parsers import parse_teacher_info

def sync_teacher_data(username, password, key, secret, query):
    token = get_access_token(username, password, key, secret)
    raw_data = fetch_teacher_data(token, query)
    return parse_teacher_info(raw_data)
