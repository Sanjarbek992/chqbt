def parse_students_response(data):
    parsed = []
    for student in data.get("results", []):
        parsed.append({
            "external_id": student.get("id"),
            "school_id": student.get("school_id"),
            "full_name": student.get("full_name"),
            "gender": student.get("gender"),
            "grade": student.get("grade"),
        })
    return parsed