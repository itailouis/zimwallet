from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class UssdSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    root_menu = db.Column(db.String(80),unique=False,nullable=False)
    menu = db.Column(db.String(120),unique=False,nullable=True)
    source = db.Column(db.Text,nullable=False)
    message = db.Column(db.Text,nullable=True)
    paramOne = db.Column(db.Text,nullable=True)
    paramTwo = db.Column(db.Text, nullable=True)
    paramThree = db.Column(db.Text,nullable=True)
    paramFour = db.Column(db.Text,nullable=True)
    paramFive = db.Column(db.Text,nullable=True)
    paramSix = db.Column(db.Text,nullable=True)
    #paramSeven = db.Column(db.Text,nullable=True)
    #paramEight = db.Column(db.Text,nullable=True)
    #paramNine = db.Column(db.Text,nullable=True)
    #paramTen = db.Column(db.Text,nullable=True)
    #paramEleven = db.Column(db.Text,nullable=True)

    #created_at = db.Column(db.DateTime,nullable=False, default=datetime.now())
    #update_at = db.Column(db.Text,nullable=False,default=datetime.now())

    def __repr__(self) -> str:
        return f'User>>>{self.source}'

