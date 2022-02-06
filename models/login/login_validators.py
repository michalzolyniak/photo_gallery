from wtforms import Form, StringField, PasswordField, validators, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models.database import db_models


class LoginValidation(Form):
    """
        Login page validations
    """
    name = StringField('name', [validators.DataRequired()])
    password = StringField('password', [validators.DataRequired()])

    @staticmethod
    def validate_name(self, name):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=name.data).first()
        if not db_user:
            self.name.errors += (ValidationError("Incorrect user name"),)

    @staticmethod
    def validate_password(self, password):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=self.name.data).first()
        if db_user:
            if not db_user.password == password.data:
                self.password.errors += (ValidationError("Incorrect password"),)


class RegisterValidation(Form):
    """
        Registration page validations
    """
    name = StringField('name', [validators.Length(min=5, max=25), validators.DataRequired()])
    password2 = PasswordField('password2')
    password = PasswordField('password', [validators.Length(min=5, max=15), validators.DataRequired(),
                                          validators.EqualTo('password2', message='Passwords must match')])

    avatar = FileField('avatar', validators=[
        FileRequired(),
        FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")
    ])

    @staticmethod
    def validate_name(self, name):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=name.data).first()
        if db_user:
            self.name.errors += (ValidationError("This user already exist"),)


class NewPasswordValidation(Form):
    """
        Change password page validations
    """
    name = StringField('name')
    old_password = StringField('old_password', [validators.DataRequired()])
    password_rep = PasswordField('password_rep', [validators.DataRequired()])
    new_password = PasswordField('new_password', [validators.Length(min=5, max=15), validators.DataRequired(),
                                          validators.EqualTo('password_rep', message='Passwords must match')])

    @staticmethod
    def validate_password(self, old_password):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=self.name.data).first()
        if db_user:
            if not db_user.password == old_password.data:
                self.old_password.errors += (ValidationError("Incorrect password"),)
