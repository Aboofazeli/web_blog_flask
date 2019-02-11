from flask import Flask, render_template, request, session, make_response
from src.models.user import User
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post


app=Flask(__name__)
app.secret_key='ali'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/logout')
def logout():
    User.logout()
    return render_template('logout.html')

@app.route('/auth/register', methods=['POST'])
def auth_register():

    email=request.form['email']

    password=request.form['password']
    User.register(email, password)

    return render_template('profile.html', email=session['email'])


@app.route('/auth/login', methods=['POST'])
def auth_login():
    email=request.form['email']
    password=request.form['password']
    user=User.login(email, password)
    if user:
        return render_template('profile.html', email=session['email'])
    else:
        return render_template('invalid_user.html')

@app.route('/blogs')
def blogs():
    if session['email']:
        blogs=Blog.blogs_from_email(session['email'])
        return render_template('blogs.html', blogs=blogs, email=session['email'])
    else:
        return render_template('index.html')


@app.route('/new_blog', methods=['POST', 'GET'])
def new_blog():
    if request.method=='GET':
        if session['email']:
            return render_template('new_blog.html')
        else:
            return render_template('index.html')
    else:
        title=request.form['title']
        description=request.form['description']
        blog=Blog(session['email'], title, description)

        blog.save_to_mongo()
        return make_response(blogs())


@app.route('/posts/<string:blog_id>')
def posts(blog_id):
    blog=Blog.from_mongo(blog_id)
    posts=blog.get_posts()
    return render_template('posts.html', posts=posts, blog_id=blog._id, blog_title=blog.title )


@app.route('/post/new/<string:blog_id>', methods=['POST', 'GET'])
def new_post(blog_id):
    if request.method=='GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title=request.form['title']
        content=request.form['content']
        post=Post(title, session['email'], content, blog_id)

        post.save_to_mongo()
        return make_response(posts(blog_id))

if __name__ == '__main__':
    app.run(port=4995, debug=True)