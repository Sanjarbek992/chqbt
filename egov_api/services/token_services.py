import requests
from django.conf import settings
from django.core.cache import cache

TOKEN_CACHE_KEY = "egov_api_token"
TOKEN_TIMEOUT = 3000  # sekundda hisoblanadi (qancha qilish kerakligini sorayman)


def get_egov_token():
    """Tizimdan yangi token olish"""
    url = "https://iskm.egov.uz:9444/oauth/token"
    data = {
        "grant_type": "password",
        "username": settings.EGOV_USERNAME,
        "password": settings.EGOV_PASSWORD,
    }
    headers = {
        "Authorization": f"Basic {settings.EGOV_BASE_AUTH}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status.code == 200:
        token = response.json().get("access_token")
        cache.set(TOKEN_CACHE_KEY, token, timeout=TOKEN_TIMEOUT)
        return token
    else:
        raise Exception(
            f"Token olishda xatolik: {response.status_code}-{response.text}"
        )


def get_cached_token():
    """Tokenni cache orqali olish yoki yangilab olish"""
    token = cache.get(TOKEN_CACHE_KEY)
    if token:
        return token
    return get_egov_token()
