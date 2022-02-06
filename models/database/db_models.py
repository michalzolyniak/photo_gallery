import flask_sqlalchemy
from constants import MAX_USERNAME_LENGTH, MAX_PASSWORD_LENGTH
db = flask_sqlalchemy.SQLAlchemy()


class User(db.Model):
    """
        User table
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_USERNAME_LENGTH), unique=True, nullable=False)
    password = db.Column(db.String(MAX_PASSWORD_LENGTH), nullable=False)

    def __repr__(self) -> str:
        return f'[User({self.id}) username={self.username}]'

    def __str__(self) -> str:
        return repr(self)


class Category(db.Model):
    """
        Category table
    """
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(MAX_USERNAME_LENGTH), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f'[User({self.id}) category={self.category}]'

    def __str__(self) -> str:
        return repr(self)


class Photo(db.Model):
    """
        Photo table
    """
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(
        db.Integer,
        nullable=False,
    )

    title = db.Column(db.String(MAX_USERNAME_LENGTH), unique=False, nullable=False)
    file_name = db.Column(db.String(MAX_USERNAME_LENGTH), unique=False, nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "category.id"
        )
    )

    category = db.relationship(
        "Category", backref="photos"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "user.id"
        )
    )

    username = db.relationship(
        "User", backref="photos"
    )

    def __repr__(self) -> str:
        return f'[User({self.id}) category={self.file_name}]'

    def __str__(self) -> str:
        return repr(self)
