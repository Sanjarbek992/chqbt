import requests
from .exceptions import EmaktabAPIError
from .parsers import parse_students_response
from egov_api.utils import get_oauth2_token

EMAKTAB_BASE_URL = "https://api.emaktab.uz"


def get_students_by_school(school_id: str):
    token = get_oauth2_token("emaktab")
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(f"{EMAKTAB_BASE_URL}/schools/{school_id}/students", headers=headers)
        response.raise_for_status()
        return parse_students_response(response.json())
    except requests.exceptions.RequestException as e:
        raise EmaktabAPIError(f"EMaktab API error: {e}")