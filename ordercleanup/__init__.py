from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from ordercleanup.config import config

db = SQLAlchemy()
mail = Mail()


def create_app(config_class=config['development']):
    app = Flask(__name__)
    app.config.from_object(config['development'])

    db.init_app(app)
    mail.init_app(app)

    from ordercleanup.errors.handlers import errors
    from ordercleanup.main.routes import main
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app