from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

# blueprints

# app specific

app = Flask(__name__)
app.config.from_object(Config)

# moment stuff
moment = Moment(app)

# db stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login stuff
login = LoginManager(app)
login.login_view = "auth.login"

# blueprints
from app.errors import bp as errors_bp

app.register_blueprint(errors_bp)
from app.auth import bp as auth_bp

app.register_blueprint(auth_bp, url_prefix="/auth")

from app import routes as routes, models as models
