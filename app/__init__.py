from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    # blueprints
    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)
    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    if not app.debug and not app.testing:
        # ... no changes here
        pass

    return app


from app import models as models
