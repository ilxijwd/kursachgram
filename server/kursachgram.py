from flask import Flask
from uuid import uuid4


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = str(uuid4())
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from models import db
    db.init_app(app)

    from auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
