import os
import connexion
from database.db import initialize_db, db
from database.models import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


basedir = os.path.abspath(os.path.dirname(__file__))

# Create the connexion application instance
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get the underlying Flask app instance
app = connex_app.app

app.config.from_envvar('ENV_FILE_LOCATION')

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
# Mongodb connection
app.config['MONGODB_HOST'] = 'mongodb://localhost/#######'

initialize_db(app)
