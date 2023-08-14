from app import bcrypt
from uuid import uuid4
from database import db
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import UUID

class User(db.Model):
    __tablename__ = 'users'
    uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    code = db.Column(db.String, nullable=True)
    code_expires = db.Column(db.DateTime, nullable=True)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as err:
            db.session.rollback()
            print(err)
            return False


    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


    def get_user_by_email(self, email: str):
        try:
            return User.query.filter_by(email=email).first()
        except Exception as err:
            print(err)
            return None

    def update_access_code(self, email: str, code: str):
        try:
            user = User.query.filter_by(email=email).first()
            if user:
                user.code = code
                user.code_expires = datetime.now() + timedelta(minutes=1)
                db.session.commit()
        except Exception as err:
            print(err)
            return None

    def verify_code(self, code):
        try:
            return True if (self.code == code and self.code_expires > datetime.now()) else False
        except Exception as err:
            print(err)
            return False 

    def __repr__(self):
        return '<User %r>' % self.uuid