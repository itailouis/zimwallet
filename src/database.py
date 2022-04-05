from flask_sqlalchemy import SQLAlchemy
from datetime  import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.Text,nullable=False)
    created_at = db.Column(db.DateTime,nullable=False, default=datetime.now())
    update_at = db.Column(db.Text,nullable=False,default=datetime.now())

    def __repr__(self) -> str:
        return f'User>>>{self.username}'