import requests
from django.conf import settings
from egov_api.services.token_services import get_cached_token
from egov_api.models.teacher_models import Teacher
from egov_api.models.school_models import School
from django.utils.dateparse import parse_date


def parse_teacher_data(data: dict) -> dict:
    """API dan kelgan o‘qituvchi obyektini model strukturasiga moslash"""
    school = School.objects.filter(ext_id=data["organizationid"]).first()

    return {
        "pinfl": data["pinfl"],
        "first_name": data["firstname"],
        "last_name": data["familyname"],
        "middle_name": data.get("lastname", ""),
        "birth_date": parse_date(data["dateofbirth"]),
        "gender": data.get("gendername", ""),
        "document_series": data.get("documentseries", ""),
        "document_number": data.get("documentnumber", ""),
        "region": data.get("regionname", ""),
        "oblast": data.get("oblastname", ""),
        "organisation_id": data["organizationid"],
        "organisation_name": data["organizationname"],
        "position_name": data.get("positioname", ""),
        "school": school,
    }


#
# def fetch_and_save_teachers_by_pinfl(pinfl: str) -> tuple:
#     """
#     PINFL orqali API’dan o‘qituvchilar ro‘yxatini olib bazaga saqlash
#     """
#     token = get_cached_token()
#     url = f"https://apimgw.egov.uz:8243/uzedu/services/school/v1/GetOrgTeachers?pinfl={pinfl}"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Accept": "application/json"
#     }
#
#     try:
#         response = requests.get(url, headers=headers, timeout=20)
#     except requests.exceptions.RequestException as e:
#         return False, f"API so‘rov xatosi: {str(e)}"
#
#     if response.status_code != 200:
#         return False, f"API xatolik: {response.status_code} - {response.text}"
#
#     result = response.json()
#     if not result.get("success", False):
#         return False, f"Xatolik: {result.get('errorMessage', 'Ma’lumot topilmadi')}"
#
#     teachers_data = result.get("result", [])
#     if not teachers_data:
#         return False, "O‘qituvchi topilmadi"
#
#     created, updated = 0, 0
#     for item in teachers_data:
#         parsed = parse_teacher_data(item)
#         obj, is_created = Teacher.objects.update_or_create(
#             pinfl=parsed["pinfl"],
#             defaults=parsed
#         )
#         if is_created:
#             created += 1
#         else:
#             updated += 1
#
#     return True, f"{created} ta yangi, {updated} ta yangilangan o‘qituvchi"
