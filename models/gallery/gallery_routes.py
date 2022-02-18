from datetime import datetime
import flask
import os
from models.database import db_models
from constants import UPLOAD_FOLDER
from models.login.login_routes import User
from models.gallery.gallery_functions import photo_data
from models.gallery.gallery_validators import CategoryValidation, PhotoValidation
from werkzeug.datastructures import CombinedMultiDict
from models.login.login_functions import login_required

# blueprint
gl = flask.Blueprint('gl', __name__, template_folder='./templates', static_folder='./static')


@gl.route('/add_photo', methods=('GET', 'POST'))
def add_photo():
    form = PhotoValidation(CombinedMultiDict((flask.request.files, flask.request.form)))
    title = flask.request.form.get('title')
    cur_category = flask.request.form.get('category')
    if flask.request.method == 'GET':
        if flask.session.get('name') is None:
            return flask.redirect('/login')
        else:
            return flask.render_template('add_photo.html', isNewPhoto=True, form=form)
    if flask.request.method == 'POST' and form.validate():
        photo = flask.request.files.get("photo")
        cur_date = datetime.now()
        cur_date = int(cur_date.strftime('%Y%m%d'))
        file_name = os.path.join(str(flask.current_app.config["UPLOAD_FOLDER"]), str(photo.filename))
        photo.save(file_name)
        obj_category = db_models.Category.query.filter_by(category=cur_category).first()
        obj_user = db_models.User.query.filter_by(username=flask.session.get('name')).first()
        new_photo = db_models.Photo(
            date=cur_date,
            title=title,
            file_name=file_name,
            category=obj_category,
            username=obj_user
        )
        db_models.db.session.add(new_photo)
        db_models.db.session.commit()
        flask.flash(f"You have just added photo: {title}")
        title = None
        cur_category = None
    return flask.render_template('add_photo.html', isNewPhoto=True, title=title,
                                 cur_category=cur_category, form=form)


@gl.route('/add_category', methods=('GET', 'POST'))
def add_category():
    form = CategoryValidation(flask.request.form)
    category = flask.request.form.get('category')
    # css_time = str(datetime.datetime.now())
    if flask.request.method == 'GET':
        if flask.session.get('name') is None:
            return flask.redirect('/login')
        else:
            return flask.render_template('add_category.html', isNewCategory=True, form=form)
    if flask.request.method == 'POST' and form.validate():
        new_category = db_models.Category(category=category)
        db_models.db.session.add(new_category)
        db_models.db.session.commit()
        flask.flash(f"You have just added category: {category}")
        category = None
    return flask.render_template("add_category.html", category=category, isNewCategory=True, form=form)


@gl.route('/', methods=('GET', 'POST'))
def gallery():
    filtered_users = []
    photos = db_models.Photo.query.all()
    css_time = str(datetime.now())
    if flask.request.method == 'GET' and flask.session.get('name') is None:
        return flask.redirect('/login')
    if flask.request.method == 'POST':
        filtered_users = flask.request.form.getlist('select_user')

        if filtered_users and filtered_users[0] != "all users":
            users = db_models.User.query.filter(db_models.User.username.in_(filtered_users)).all()
            photos = db_models.Photo.query.filter(db_models.Photo.user_id.in_([user.id for user in users])).all()
    return flask.render_template("gallery.html", isGallery=True, photo_data=photo_data(photos),
                                 filtered_users=filtered_users, time=css_time)


@gl.route('/uploaded/<filename>')
def uploaded(filename):
    return flask.send_from_directory(UPLOAD_FOLDER, filename)


@gl.route('/uploaded_avatar/<filename>')
def uploaded_avatar(filename):
    return flask.send_from_directory(os.path.join(UPLOAD_FOLDER, "avatars"), filename)


@gl.app_context_processor
def inject_user():
    return {
        "user": User.current()
    }


@gl.app_context_processor
def inject_users():
    users = db_models.User.query.all()
    users_data = []
    for user in users:
        users_data.append(user.username)
    return {
        "db_users": users_data
    }


@gl.app_context_processor
def inject_categories():
    db_categories = db_models.Category.query.all()
    categories = []
    for cat in db_categories:
        categories.append(cat.category)
    return {
        "db_categories": categories
    }


