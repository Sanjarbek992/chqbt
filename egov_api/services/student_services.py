import requests
from django.conf import settings
from egov_api.services.token_services import get_cached_token
from egov_api.models.student_models import Student
from egov_api.models.school_models import School
from django.utils.dateparse import parse_date


def parse_student_data(data: dict) -> dict:
    """
    API JSON dan Student modeliga mos dict shalga aylantirish
    """
    school = School.objects.get(ext_id=data["organizationid"]).first()

    return {
        "pinfl": data["pinfl"],
        "full_name": data["fullName"],
        "birth_date": parse_date(data["dateOfBirth"]),
        "gender": data["genderName"],
        "document_series": data.get("documentseries", ""),
        "document_number": data.get("documentnumber", ""),
        "mfy_name": data.get("mfyname", ""),
        "grade": data.get("schoolGradeName", ""),  # misol: "2-синф"
        "class_letter": data.get("orgschoolGradeName", ""),  # misol: "2-V"
        "school": school,
        "school_year": data.get("schoolyearname", ""),
        "address": data.get("adress", ""),
        "oblast_id": data.get("oblastid"),
        "region_id": data.get("regionid"),
        "school_grade_id": data.get("schoolgradeid"),
        "org_school_grade_id": data.get("orgschoolgradeid"),
        "school_year_id": data.get("schoolyearid"),
        "mfy_id": data.get("mfyid"),
    }


# def fetch_and_save_student_by_pinfl(pinfl: str) -> tuple:
#     """
#     PINFL orqali API'dan o‘quvchini olish va bazaga saqlash
#     """
#     token = get_cached_token()
#     url = f"https://apimgw.egov.uz:8243/uzedu/services/school/v1/ChildrenInfoWithPINFL?pinfl={pinfl}&lang=uz_cyrl"
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
#     student_data = parse_student_data(result["result"])
#
#     obj, created = Student.objects.update_or_create(
#         pinfl=student_data["pinfl"],
#         defaults=student_data
#     )
#
#     status = "yaratildi" if created else "yangilandi"
#     return True, f"O‘quvchi {status}: {obj.full_name}"
