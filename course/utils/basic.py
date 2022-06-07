
def get_invalid_msg(msg):
    return {
        "status_code": 200,
        "message": msg
    }


def get_response_data(data):
    return {
        "status_code": 200,
        "result": data
    }


def get_success_msg():
    return {
        "status_code": 200,
        "message": "success"
    }
