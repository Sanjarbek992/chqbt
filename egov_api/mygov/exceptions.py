class MyGovAPIError(Exception):
    def __init__(self, message, status):
        super().__init__(f"API Error {status}: {message}")

class MyGovAuthError(Exception):
    def __init__(self, message, status):
        super().__init__(f"Auth Error {status}: {message}")
