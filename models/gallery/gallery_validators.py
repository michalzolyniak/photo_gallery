from wtforms import Form, StringField, validators, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models.database import db_models


class CategoryValidation(Form):
    """
        Category page validations
    """
    category = StringField('category', [validators.Length(min=4, max=25), validators.DataRequired()])

    def validate_category(self, name):
        category_name: db_models.User | None = db_models.Category.query.filter_by(category=name.data).first()
        if category_name:
            self.category.errors += (ValidationError("This category already exist"),)


class PhotoValidation(Form):
    """
        Add new photo page validations
    """
    title = StringField('title', [validators.Length(min=4, max=25), validators.DataRequired()])

    photo = FileField('photo', validators=[
        FileRequired(),
        FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")
    ])

    category = StringField('category', [validators.DataRequired()])

