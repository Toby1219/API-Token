from flask import Blueprint, request, jsonify, make_response
from ..models.model import User, Blacklist
from .. import db, Config, jwt
from datetime import datetime
from ..extension.utils import message_handler, token_times
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required

auth_bp = Blueprint('auth_bp', __name__)

# Not a route
@jwt.token_in_blocklist_loader
def check_if_token_is_blocked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(Blacklist.id).filter_by(jti=jti).first()
    return True if token else False

@auth_bp.route('/register', methods=["POST"])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data["username"]).first():
        return jsonify(message_handler("user already exist", "", ok=False)), 409
    user = User(username=data['username'], role='user')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message_handler("User created succesfully (Login to get acsess token)", "")), 201

@auth_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        user.check_password(data['password'])
        token = create_access_token(identity=user.username, 
                                    additional_claims={'role':user.role},
                                    expires_delta=Config.JWT_ACCESS_TOKEN_EXPIRES)        
        refresh_token_ = create_refresh_token(identity=user.username, 
                                             additional_claims={'role':user.role},
                                             expires_delta=Config.JWT_REFRESH_TOKEN)
        issued = datetime.now()
        exp = issued + Config.JWT_ACCESS_TOKEN_EXPIRES
        
        return jsonify(message_handler("Login sucessful API key crated",
                                       {"token":token, "refresh_token": refresh_token_,
                                        "role":f"{user.role}",
                                        "Token Issued": f"at: ({issued})",
                                        "Token Expiress": f"at: ({exp})"}, write=True)), 200
        
    return jsonify(message_handler("Invalid credentials",{"token":""}, ok=False)), 401

@auth_bp.route('/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():    
    identity = get_jwt_identity()
    claims = get_jwt()
    issued, exp = token_times(get_jwt)
    new_token = create_access_token(identity=identity, additional_claims={'role':claims.get('role')})
    msg = message_handler("New Token created", 
                               {"new token":new_token, 
                                "Token Issued": f"at: ({issued})", 
                                "Token Expiress": f"at: ({exp})"})
    response =  make_response(msg, 200, {"Authorization": f'Bearer {new_token}'})
    # print("\n", response.headers, "\n")
    return response

@auth_bp.route('/whoami', methods=["GET"])
@jwt_required()
def who_am_i():
    user_ = get_jwt()
    issued, exp = token_times(get_jwt)
    return jsonify(message_handler("This is the curent user", 
                                   {"Current user":f"{user_.get('sub')}", "Role":f"{user_.get("role")}",
                                    "Token Issued": f"at: ({issued})",
                                    "Token Expiress": f"at: ({exp})"})), 200


@auth_bp.route('/logout', methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    db.session.add(Blacklist(jti=jti))
    db.session.commit()
    return jsonify(message_handler("Log out sucessful API key blacklisted",
                                {"blacklisted_token":jti,
                                "Time": f"{datetime.now()}"})), 200

    

