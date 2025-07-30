from flask import request,Blueprint,jsonify
from flask_jwt_extended import create_access_token

from model import db,User
auth_bp = Blueprint('auth', __name__,url_prefix='/auth')
from extensions import cache
from .admin import find_all_users


# Register User
@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'msg':'User already exists!'}),400

    user = User(email=data['email'],fullname=data['fullname'])
    if 'address' in data:
        user.address = data["address"]
    user.set_password(data['password'])
    access_token = create_access_token(identity=user.email)
    db.session.add(user)
    db.session.commit()

    # Delete users cache
    cache.delete_memoized(find_all_users)

    return jsonify(access_token = access_token),201

# Login User
@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'msg':'User does not exist with this email!'}),400

    if not user.check_password(data['password']):
        return jsonify({'msg':'Incorrect Password!'})

    access_token = create_access_token(identity=user.email)
    return jsonify(access_token = access_token),200