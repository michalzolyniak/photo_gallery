from models.login.user_class import User
from models.database import db_models
from models.login.login_validators import LoginValidation, RegisterValidation, NewPasswordValidation, ChangeUserDataValidation
from werkzeug.datastructures import CombinedMultiDict
from models.login.login_functions import login_required
from models.database import db_models
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
    name = flask.request.form.get('name')
    form = NewPasswordValidation(flask.request.form)
    if flask.request.method == 'POST' and form.validate():
        password = flask.request.form.get('new_password')
        db_models.User.query.filter(db_models.User.username == str(name)).update({'password': password})
        db_models.db.session.commit()
        flask.flash(f"You have just changed your password")
    return flask.render_template("change_password.html", isNewPassword=True, form=form, name=name)


@lg.route('/remove_account', methods=('GET', 'POST'))
def remove_account():
    if flask.request.method == 'POST':
        if flask.request.form['action'] == 'Yes':
            users_id = db_models.User.query.filter(db_models.User.username == str(flask.session['name'])).first().id
            db_models.Photo.query.filter(db_models.Photo.user_id == users_id).delete()
            db_models.User.query.filter(db_models.User.username == str(flask.session['name'])).delete()
            db_models.db.session.commit()
            flask.session.clear()
            flask.flash(f"Your account has been removed")
            return flask.redirect('/register')
        elif flask.request.form['action'] == 'No':
            return flask.redirect('/user_settings')
    return flask.render_template("remove_account.html", isRemoveAccount=True)


@lg.route('/change_user_data', methods=('GET', 'POST'))
def change_user_data():
    new_name = flask.request.form.get('new_name')
    avatar = flask.request.files.get("avatar")
    form = ChangeUserDataValidation(flask.request.form)
    if flask.request.method == 'POST' and form.validate():
        if new_name:
            db_models.User.query.filter(db_models.User.username == str(flask.session['name'])).update({'username': new_name})
            db_models.db.session.commit()
        if avatar:
            db_models.User.query.filter(db_models.User.username == str(new_name)).update({'username': new_name})
            db_models.db.session.commit()
        # flask.session['name'] = flask.request.form.get('new_name')
        if new_name and avatar:
            flask.session['name'] = new_name
            flask.flash(f"You have just changed your name and avatar.")
        elif new_name:
            flask.session['name'] = new_name
            flask.flash(f"You have just changed your name.")
        elif avatar:
            flask.flash(f"You have just changed your avatar")
        else:
            flask.flash(f"Please fill a new name or choose a new avatar")
    return flask.render_template("user_data.html", isUserData=True, form=form, name=new_name)


@lg.route('/logout')
@login_required
def logout():
    flask.session.clear()
    return flask.redirect('/login')