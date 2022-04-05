from flask import Blueprint, Response
from functools import wraps


ussdentry = Blueprint("ussdentry", __name__, url_prefix="/ussd/econet/main")


def returns_xml(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/xml; charset=utf-8')

    return decorated_function


@ussdentry.post("/entry")
@returns_xml
def main():
    return {"message": "hello world"}


@ussdentry.get("/hello")
def test():
    return {"message": "hello world"}
