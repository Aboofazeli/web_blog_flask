import uuid
from src.models.post import Post
import datetime
from src.common.database import Database



class Blog:
    def __init__(self, author, title, description, _id=None):
        self.author=author
        self.title=title
        self.description=description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):

        post=Post(title=title, author=self.author, content=content, date=date, blog_id=self._id)
        post.save_to_mongo()

    def json(self):
        return {'author': self.author, 'title': self.title, 'description':self.description, '_id': self._id}

    def save_to_mongo(self):
        Database.insert(collection='blogs', data=self.json())

    def get_posts(self):
        return Post.from_blog(self._id)

    @staticmethod
    def blogs_from_email(email):
        blogs = Database.find('blogs', {'author': email})
        return [blog for blog in blogs]

    @classmethod
    def from_mongo(cls, id):
        blog_data = Database.find_one(collection='blogs',
                                      query={'_id': id})
        return cls(author=blog_data['author'],
                   title=blog_data['title'],
                   description=blog_data['description'],
                   _id=blog_data['_id'])


