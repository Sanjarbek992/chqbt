import logging
import requests
from django.conf import settings
from django.core.cache import cache
from users.models import CustomUser

logger = logging.getLogger(__name__)

CACHE_TIMEOUT = 60 * 10  # 10 daqiqa

def create_oauth2_tokens(username: str, password: str, use_cache: bool = False) -> dict:
    """
    OAuth2 password grant orqali access va refresh token olish funksiyasi.

    :param username: Foydalanuvchi nomi
    :param password: Foydalanuvchi paroli
    :param use_cache: True bo‘lsa, tokenlar Redis orqali keshlanadi
    :return: access_token, refresh_token, expires_in, token_type
    :raises: Exception (agar token olinmasa yoki foydalanuvchi yaroqsiz bo‘lsa)
    """

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        raise Exception("Bunday foydalanuvchi mavjud emas.")

    # Faqat superadmin va admin foydalanuvchilar uchun ruxsat beramiz
    if user.role not in ['superadmin', 'admin']:
        raise Exception("Ushbu grant faqat admin yoki superadminlar uchun ruxsat etilgan.")

    # Caching
    cache_key = f"oauth2_token:{username}"
    if use_cache:
        cached_token = cache.get(cache_key)
        if cached_token:
            logger.debug(f"Token Redis cache’dan olindi: {username}")
            return cached_token

    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': settings.OAUTH2_CLIENT_ID,
        'client_secret': settings.OAUTH2_CLIENT_SECRET,
    }

    url = f"{settings.BASE_OAUTH_URL}/o/token/"
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Token olishda xatolik: {e}")
        raise Exception("Token olishda xatolik yuz berdi. Tafsilotlar logda.")

    token_data = response.json()

    if use_cache:
        cache.set(cache_key, token_data, timeout=CACHE_TIMEOUT)
        logger.debug(f"Token Redis cache’da saqlandi: {username}")

    return token_data


MAX_ATTEMPTS = 5
BLOCK_MINUTES = 30


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
