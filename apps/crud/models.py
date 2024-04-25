from datetime import datetime

from apps.app import db
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = "users"

    # primary_key : 이 데이터를 상징하는 식별값
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )

    # getter
    @property
    def password(self):
        raise AttributeError("읽어 들일 수 없음")
    
    # setter
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)