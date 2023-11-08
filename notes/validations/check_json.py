from rest_framework.exceptions import ParseError


def check_json(func):
    def wrapper():
        try:
            func()
        except ParseError as e:
            return {"error": True, "message": e}

    return wrapper()