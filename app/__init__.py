from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .extension.config import Config
from .extension.utils import message_handler

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    
    from .routes.auth import auth_bp
    from .routes.views import w_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(w_bp, url_prefix='/api')
    
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify(message_handler(
            "Token has expired you have to get a new token", '', ok=False)), 401
    
    @jwt.invalid_token_loader
    def invalid_token(error):
        return jsonify(message_handler(
            "Invalid Token ", '', ok=False)), 401
    
    @jwt.unauthorized_loader
    def missing_token(error):
        return jsonify(message_handler(
            "Missing Token: enter in you header Authority: Barer <token>", '', ok=False)), 401
    
    @jwt.revoked_token_loader
    def revoked_token(jwt_header, jwt_payload):
        #Blacllsted tokens
        return jsonify(message_handler(
            "Bloced Token: get a new by login token>", '', ok=False)), 401
       
    def createfile():
        import os 
        if not os.path.exists("instance"):
            os.mkdir("instance")
        try:
            with open(f"./instance/tokens.json", "x") as f:
                pass
        except:
            pass
            
    createfile()
    
    return app