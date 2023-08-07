from flask import Blueprint, request, jsonify, make_response, session
import json
from sqlalchemy import exc
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.users import Users

from utils.security import security
from utils.forms_user import RegiterForm
from utils.forms_user import LoginForm

from utils.db import db


users = Blueprint('users',__name__)

#registrar usuario
@users.route('/register/user', methods=['POST'])
def register_user():
    form = RegiterForm(request.form)
    print(form.data)
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='scrypt')
        new_user = Users(email=form.email.data, 
                        password=hashed_password, 
                        name=form.name.data, 
                        phone_number=form.phone_number.data)
        try:
            db.session.add(new_user)
            db.session.commit()     
            return make_response(jsonify({"message": "Registered successfully!"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
    else:
        return make_response(jsonify({"message": "Form submission invalid"}), 400)

#iniciar sesion usuario
@users.route('/login/user', methods=['POST'])
def login():
    form = LoginForm(request.form)
    print(form.data)
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            encode_token = security.generate_token_user(user)
            response = {
                'message': 'Logged in successfully.',
                'encode_token': encode_token,
                'user': user.id
            }
            return jsonify(response)
        else:
            return jsonify({'message' : 'Invalid email or password.'}), 401
    return jsonify({'message' : 'Invalid form data.'}), 400


