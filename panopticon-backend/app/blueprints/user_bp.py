from flask_jwt_extended import jwt_required, get_jwt_identity, fresh_jwt_required, create_access_token, create_refresh_token
from flask import Blueprint, request, signals, Response, abort, jsonify
from app import User
from werkzeug.security import generate_password_hash, check_password_hash

user_bp = Blueprint("user_bp", __name__, url_prefix='/users')

@user_bp.route('/register', methods=["POST"])
def register():
    content = request.json
    print(content)
    user = User()
    user.name = content["name"]
    user.email = content["email"]
    user.password = generate_password_hash(content["password"])
    user.save()
    access_token = create_access_token(identity=str(User.id), fresh=True)
    return jsonify(access_token=access_token), 200

@user_bp.route('/login', methods=["POST"])
def login():
    content = request.json
    user = User.objects(email=content["email"]).first()
    if user and check_password_hash(user.password, content["password"]):
        access_token = create_access_token(identity=str(user.id), fresh=True)
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    abort(401)


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    ret = {'access_token': new_token}
    return jsonify(ret), 200
    
