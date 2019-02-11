from src.common.database import Database
import datetime
import uuid


class Post:
    def __init__(self, title, author, content, blog_id, date=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.author = author
        self.date = date
        self.content = content
        self.blog_id = blog_id
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return {'author': self.author,
                'title': self.title,
                'content': self.content,
                'blog_id':self.blog_id,
                'date': self.date,
                '_id': self._id}

    @staticmethod
    def from_mongo(id):
        post_data = Database.find_one(collection='posts', query={'_id': id})
        return post_data

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]



