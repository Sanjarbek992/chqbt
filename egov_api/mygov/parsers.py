def parse_teacher_info(api_response: dict) -> dict:
    return {
        "full_name": api_response.get("fullName"),
        "birth_date": api_response.get("birthDate"),
        "degree": api_response.get("degree"),
        "specialty": api_response.get("specialty"),
        "university": api_response.get("university"),
        "category": api_response.get("category"),
        "experience": api_response.get("experience"),
    }
