from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.get("/")
def index():
    return {"message": "hello world"}


@auth.get("/hello")
def home():
    return {"message": "hello world"}
