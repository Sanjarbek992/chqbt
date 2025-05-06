from .api import get_students_by_school
from .models import EmaktabStudent

def sync_students(school_id):
    students = get_students_by_school(school_id)
    for s in students:
        EmaktabStudent.objects.update_or_create(
            external_id=s["external_id"],
            defaults={
                "school_id": s["school_id"],
                "full_name": s["full_name"],
                "gender": s["gender"],
                "grade": s["grade"],
            },
        )
