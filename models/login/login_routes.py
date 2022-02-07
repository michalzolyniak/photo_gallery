from models.login.user_class import User
from models.database import db_models
from models.login.login_validators import LoginValidation, RegisterValidation, NewPasswordValidation
from werkzeug.datastructures import CombinedMultiDict
from models.login.login_functions import login_required
import flask

# blueprint
lg = flask.Blueprint('lg', __name__, template_folder='./templates', static_folder='./static')


@lg.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginValidation(flask.request.form)
    name = flask.request.form.get('name')
    if flask.request.method == 'POST' and form.validate():
        flask.session['name'] = name
        return flask.redirect('/')
    return flask.render_template("login.html", isLogin=True, form=form, name=name)


@lg.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterValidation(CombinedMultiDict((flask.request.files, flask.request.form)))
    name = flask.request.form.get('name')
    if flask.request.method == 'POST' and form.validate():
        flask.flash(f"You just registered user: {name}.Please login.")
        password = flask.request.form.get('password')
        avatar = flask.request.files.get("avatar")
        new_user = db_models.User(username=name, password=password)
        db_models.db.session.add(new_user)
        db_models.db.session.commit()
        avatar.save(flask.current_app.config["UPLOAD_FOLDER"] + "/" + f"{name}.jpg")
        name = None
    return flask.render_template("register.html", isRegister=True, form=form, name=name)


@lg.route('/user_settings', methods=('GET', 'POST'))
def user_settings():
    return flask.render_template("user_settings.html", isSettings=True)


@lg.route('/change_password', methods=('GET', 'POST'))
def change_password():
    name = User.current().name
    form = NewPasswordValidation(CombinedMultiDict((flask.request.files, flask.request.form)))
    if flask.request.method == 'POST' and form.validate():
        password = flask.request.form.get('new_password')
        # user_to_update = User.query.filter_by(username=name).first()
        # user_to_update.data = {'password': password}
        # db_models.db.session.commit()
        flask.flash(f"You have just changed a password")
    return flask.render_template("change_password.html", isNewPassword=True, form=form, name=name)


@lg.route('/logout')
@login_required
def logout():
    flask.session.clear()
    return flask.redirect('/login')

