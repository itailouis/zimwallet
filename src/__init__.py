from flask import Flask
from src.auth import auth
from src.database import db
from src.controllers.ussdentry import ussdentry
from src.models.messageRequest import MessageRequest
from src.models.messageResponse import MessageResponse
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI")
        )
    else:
        app.config.from_mapping(test_config)
    db.app = app
    db.init_app(app)

    #if os.path.exists('zimwallet.db')==False:
    db.create_all()

    # Create the database


    # app.response_class = MessageResponse
    # app.request_class = MessageRequest
    app.register_blueprint(ussdentry)
    app.register_blueprint(auth)
    return app
