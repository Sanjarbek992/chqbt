import requests
from .exceptions import MyGovAPIError, MyGovAuthError
from egov_api.utils import get_base64_auth_header

BASE_URL = "https://iskm.egov.uz:9444"
TOKEN_ENDPOINT = "/oauth2/token"
API_ENDPOINT = "/api/teacher-info"


def get_access_token(username: str, password: str, consumer_key: str, consumer_secret: str) -> str:
    url = BASE_URL + TOKEN_ENDPOINT
    headers = {
        "Authorization": get_base64_auth_header(consumer_key, consumer_secret),
    }
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        raise MyGovAuthError("Token olishda xatolik", response.status_code)
    return response.json().get("access_token")


def fetch_teacher_data(token: str, query_params: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(BASE_URL + API_ENDPOINT, headers=headers, params=query_params)
    if response.status_code != 200:
        raise MyGovAPIError("Ma'lumot olishda xatolik", response.status_code)
    return response.json()