import constants
import os

UPLOAD_FOLDER = os.path.dirname(constants.__file__)
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'models\database\photos')

MAX_USERNAME_LENGTH = 30
MAX_PASSWORD_LENGTH = 100

