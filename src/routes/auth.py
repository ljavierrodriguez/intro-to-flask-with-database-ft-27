import datetime
from flask import Blueprint, jsonify, request, abort, json
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

bpAuth = Blueprint("bpAuth", __name__)

@bpAuth.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return jsonify({ "error": "username is required"}), 400

        if not password:
            return jsonify({ "error": "password is required"}), 400
        
        user = User.query.filter_by(username=username).first()

        if not user:
            return jsonify({ "error": "username/password are incorrects"}), 401

        if not check_password_hash(user.password, password):
            return jsonify({ "error": "username/password are incorrects"}), 401

        payload = {
            "id": user.id,
            "username": user.username
        } 

        expire = datetime.timedelta(days=1)
        
        # el valor a asignar a identity debe ser un string
        access_token = create_access_token(identity=json.dumps(payload), expires_delta=expire)

        return jsonify({ "status": "Login successfully", "access_token": access_token }), 200


    except Exception as e:
        print(e)
        abort(500)


@bpAuth.route('/register', methods=['POST'])
def register():
    
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username:
            return jsonify({ "error": "username is required"}), 400

        if not password:
            return jsonify({ "error": "password is required"}), 400
        
        found = User.query.filter_by(username=username).first()

        if found:
            return jsonify({ "error": "username is already in use"}), 400

        user = User()
        user.username = username
        user.password = generate_password_hash(password)

        db.session.add(user)
        db.session.commit()
 
        payload = {
            "id": user.id,
            "username": user.username
        } 

        expire = datetime.timedelta(days=1)
        
        # el valor a asignar a identity debe ser un string
        access_token = create_access_token(identity=json.dumps(payload), expires_delta=expire)

        return jsonify({ "status": "Register successfully", "access_token": access_token }), 200


    except Exception as e:
        print(e)
        abort(500)