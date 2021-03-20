from flask import Blueprint
from flask import request as req
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    email = req.form.get('email')
    password = req.form.get('password')
    remember = True if req.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return 'invalid credentials', 401

    return 'ok', 200


@auth_bp.route('/register', methods=['POST'])
def register():
    email = req.form.get('email')
    name = req.form.get('name')
    password = req.form.get('password')
    remember = True if req.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if user:
        return 'this email is already in use', 409

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return 'ok', 201
