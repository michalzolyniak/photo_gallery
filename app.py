import models.database.db_models
import models.gallery.gallery_routes
import models.login.templates
import flask
import models
import models.database.db_models
import os
from constants import UPLOAD_FOLDER


def init_app():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app = flask.Flask(__name__, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY="key",
        SQLALCHEMY_DATABASE_URI="sqlite:///models/database/db_photo.sqlite3",
        UPLOAD_FOLDER=UPLOAD_FOLDER,
    )
    app.register_blueprint(models.gallery.gallery_routes.gl)
    app.register_blueprint(models.login.login_routes.lg)

    models.database.db_models.db.init_app(app)
    with app.app_context():
        models.database.db_models.db.create_all()
    return app


app = init_app()




