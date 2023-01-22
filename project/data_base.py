from peewee import *
from datetime import datetime
from playhouse.mysql_ext import MySQLConnectorDatabase
import hashlib
from local_settings import USER_DATABASE, PASSWORD_DATABASE
database = MySQLConnectorDatabase(
    "danielbd",
    user=USER_DATABASE,
    password=PASSWORD_DATABASE,
    host="127.0.0.1",
    port=3306
)


class User(Model):  # hereda de model una tabla
    user_name = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = "users"

    @classmethod
    def authenticate(cls, username, password):

        user = cls.select().where(User.user_name == username).first()
        if user and user.password == cls.create_password(password):
            return user

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode("utf-8"))
        return h.hexdigest()


class Movie(Model):
    imdbID = CharField(max_length=50)
    title = CharField(max_length=50)
    year = CharField(max_length=4)
    genre = CharField(max_length=50)
    director = CharField(max_length=50)
    actors = CharField(max_length=50)
    plot = CharField(max_length=250)
    poster = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = "movies"


class UserReview(Model):
    user = ForeignKeyField(User, backref="reviews")
    movie = ForeignKeyField(Movie, backref="reviews")
    reviews = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

    class Meta:
        database = database
        table_name = "user_reviews"
