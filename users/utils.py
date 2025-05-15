import requests
from django.conf import settings

def create_oauth2_tokens(user):
    data = {
        'grant_type': 'password',
        'username': user.username,
        'password': user.raw_password,
        'client_id': settings.OAUTH2_CLIENT_ID,
        'client_secret': settings.OAUTH2_CLIENT_SECRET,
    }

    url = f"{settings.BASE_OAUTH_URL}/o/token/"

    response = requests.post(url, data=data)

    if response.status_code != 200:
        raise Exception("Token olishda xatolik: " + response.text)

    return response.json()

from django.core.cache import cache
from datetime import timedelta

MAX_ATTEMPTS = 5
BLOCK_MINUTES = 3

def get_login_cache_key(username):
    return f"login_attempts:{username}"

def get_block_key(username):
    return f"login_blocked:{username}"

def increment_login_attempt(username):
    key = get_login_cache_key(username)
    attempts = cache.get(key, 0) + 1
    cache.set(key, attempts, timeout=60 * BLOCK_MINUTES)  # harakatlar 30 daqiqaga saqlanadi
    return attempts

def is_user_blocked(username):
    return cache.get(get_block_key(username)) is not None

def block_user(username):
    cache.set(get_block_key(username), True, timeout=60 * BLOCK_MINUTES)

def reset_login_attempts(username):
    cache.delete(get_login_cache_key(username))
    cache.delete(get_block_key(username))
