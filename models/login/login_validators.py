from wtforms import Form, StringField, PasswordField, validators, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models.database import db_models
from models.login.user_class import User


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
    new_password = PasswordField('new_password', [validators.Length(min=5, max=15), validators.DataRequired()])
    password_rep = PasswordField('password_rep', [validators.Length(min=5, max=15), validators.DataRequired(),
                                                  validators.EqualTo('new_password', message='new passwords must match')])

    def validate_old_password(self, filed):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=self.name.data).first()
        if db_user:
            if not db_user.password == filed.data:
                self.old_password.errors += (ValidationError("Incorrect old password"),)

    def validate_new_password(self, filed):
        if filed.data:
            if self.old_password.data == filed.data:
                self.new_password.errors += (ValidationError("new password has to be different then old"),)


class ChangeUserDataValidation(Form):
    """
        Change user data validations
    """

    new_name = StringField('new_name', [validators.Length(min=5, max=25), validators.Optional()])

    avatar = FileField('avatar', validators=[
        FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")
    ])

    @staticmethod
    def validate_new_name(self, new_name):
        db_user: db_models.User | None = db_models.User.query.filter_by(username=new_name.data).first()
        if db_user:
            self.new_name.errors += (ValidationError("This user already exist"),)


    # old_password = StringField('old_password', [validators.DataRequired()])
    # password_rep = PasswordField('password_rep', [validators.DataRequired()])
    # new_password = PasswordField('new_password', [validators.Length(min=5, max=15), validators.DataRequired()])
    # password_rep = PasswordField('password_rep', [validators.Length(min=5, max=15), validators.DataRequired(),
