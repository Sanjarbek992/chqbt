import logging
import requests

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def safe_request(method, url, headers=None, data=None, json=None, timeout=10):
    try:
        response = requests.request(method, url, headers=headers, data=data, json=json, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise TimeoutError("So‘rov muddati tugadi")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP xato: {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Tarmoq xatosi: {str(e)}")
def get_base64_auth_header(consumer_key, consumer_secret):
    import base64
    auth_str = f"{consumer_key}:{consumer_secret}"
    return base64.b64encode(auth_str.encode()).decode()
