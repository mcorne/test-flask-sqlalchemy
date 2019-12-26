from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.sqlite3"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    category = db.relationship("Category", backref=db.backref("posts", lazy=True))

    def __repr__(self):
        return "<Post %r>" % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Category %r>" % self.name


db.drop_all()
db.create_all()

admin = User(username="admin", email="admin@example.com")
guest = User(username="guest", email="guest@example.com")
db.session.add(admin)
db.session.add(guest)
db.session.commit()

print("User.query.all: ", end="")
print(User.query.all())
print("User.query.filter_by: ", end="")
print(User.query.filter_by(username="admin").first())

py = Category(name="Python")
Post(title="Hello Python!", body="Python is pretty cool", category=py)
p = Post(title="Snakes", body="Ssssssss")
py.posts.append(p)
db.session.add(py)
db.session.commit()

print("posts: ", end="")
print(py.posts)

from sqlalchemy.orm import joinedload

query = Category.query.options(joinedload("posts"))
for category in query:
    print("category: ", end="")
    print(category, category.posts)

print("posts: ", end="")
print(Post.query.with_parent(py).filter(Post.title != "Snakes").all())

