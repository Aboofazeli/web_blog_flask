from src.common.database import Database
from src.models.blog import Blog
from flask import session
import uuid


class User:
    def __init__(self, email, password, _id=None):
        self.email=email
        self.password=password
        self._id = uuid.uuid4().hex if _id is None else _id


    @classmethod
    def register(cls, email, password):
        new_user=cls(email, password)
        new_user.save_to_mongo()
        session['email']=email

    @staticmethod
    def login(email, password):
        user=Database.find_one('users',{'email':email})
        if user:
            if password == user['password']:
                session['email']=email
                return True
            else:
                session['email']=None
                return
        session['email']=None
        return False

    @staticmethod
    def logout():
        session['email']=None
    def json(self):
        return {'email': self.email,
                'password': self.password,
                '_id':self._id}

    def save_to_mongo(self):
        Database.insert('users', self.json())

