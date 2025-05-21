import requests
from django.conf import settings
from egov_api.services.token_services import get_cached_token
from egov_api.models.school_models import School


def parse_school_data(item):
    """
    API dan kelgan bitta maktab obyektini School model strukturasiga moslab tayyorlash
    """
    return {
        "ext_id": item["ext_id"],
        "inn": item["schoolinn"],
        "name": item["schoolfullname"],
        "short_name": item["schoolhortname"],
        "address": item.get("address", ""),
        "region_id": item["regionid"],
        "region": item.get("regionname", ""),
        "region_soato_code": item.get("regionsoatocode", ""),
        "oblast_id": item["oblastid"],
        "oblast": item.get("oblastname", ""),
        "oblast_soato_code": item.get("oblastsoatocode", ""),
        "director": item.get("directir", ""),
        "contact_info": item.get("contactinfo", ""),
        "latitude": item.get("latitude"),
        "longitude": item.get("longitude"),
    }
#
# def fetch_and_save_schools_bysoato(soato_code: str) -> tuple:
#     """
#     Berilgan SOATO kodi asosida maktablar r`yxatini olish va bazaga saqlash
#     """
#     token = get_cached_token()
#     url = f"https://apimgw.egov.uz:8243/uzedu/services/school/v1/GetSchoolsBySoatoCode?soatoCode={soato_code}"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json",
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=20)
#     except requests.exceptions.RequestException as e:
#         return False, f"API so`rov xatosi: {str(e)}"
#     if response.status_code != 200:
#         return False, f"API xatolik: {response.status_code} - {response.text}"
#     result = response.json()
#     if not result.get("success", False):
#         return False, f"API muvaffaqiyatsiz: {result.get('errorMessage')}"
#
#     schools_data = result.get("result", [])
#     created, updated = 0, 0
#
#     for item in schools_data:
#         parsed = parse_school_data(item)
#         obj, is_created = School.objects.update_or_create(
#             ext_id=parsed["ext_id"],
#             defaults=parsed
#         )
#         if is_created:
#             created += 1
#         else:
#             updated += 1
#
#     return True, f"{created} ta yangi, {updated} ta yangilangan maktab."
