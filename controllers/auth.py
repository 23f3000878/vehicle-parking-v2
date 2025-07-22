from flask import request,Blueprint,jsonify
from flask_jwt_extended import create_access_token
from model import db,User
auth_bp = Blueprint('auth', __name__,url_prefix='/auth')


# Register User
@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({'msg':'User already exists!'}),400

    user = User(username=data['username'],fullname=data['fullname'])

    user.set_password(data['password'])
    access_token = create_access_token(identity=user.username)
    db.session.add(user)
    db.session.commit()
    return jsonify(access_token = access_token),201

# Login User
@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'msg':'User does not exist with this username!'}),400

    if not user.check_password(data['password']):
        return jsonify({'msg':'Incorrect Password!'})

    access_token = create_access_token(identity=user.username)
    return jsonify(access_token = access_token),200