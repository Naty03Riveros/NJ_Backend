def http_response_object(success: bool, message: str, data: dict, code: int):
    response = {
        'success': success,
        'message': message,
        'data': data
    }
    return response, code
