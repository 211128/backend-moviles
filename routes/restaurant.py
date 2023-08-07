from flask import Blueprint, request, jsonify, make_response, session
import json

from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from models.restuarants import Departments


from utils.form_rstaurant import RegiterForm
from utils.form_rstaurant import LoginForm
from utils.security import security

from werkzeug.utils import secure_filename
from firebase_admin import storage 

from utils.db import db

departments = Blueprint('departments',__name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#registrar department
@departments.route('/register/department', methods=['POST'])
def register_department():
    form = RegiterForm()

    print(form)
  
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,  method='scrypt')
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            blob = storage.bucket().blob(filename)
            blob.upload_from_string(
                file.read(),

                content_type=file.content_type
            )
            blob.make_public()
            image_url = blob.public_url
        else:
            return "Invalid image", 400
        new_user = Departments(
                        name=form.name.data, 
                        email=form.email.data,
                        password=hashed_password,
                        image_url=image_url, 
                        name_department=form.name_department.data, 
                        description=form.description.data,
                        contacto=form.contacto.data,
                        )
        try:
            db.session.add(new_user)
            db.session.commit()     
            return make_response(jsonify({"message": "Registered successfully!"}), 200)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)
    else:
        return make_response(jsonify({"message": "Form submission invalid"}), 400)


#listar los restaurantes
@departments.route("/api/department/list", methods=['GET'])
def get_all_restaurants():
    has_acces = security.verify_token_user(request.headers)
    if has_acces:
        all_restaurants = Departments.query.all()
        if not all_restaurants:
            return jsonify({'message' : 'No restaurants found.'}), 404

        restaurants_list = []
        for restaurant in all_restaurants:
            restaurants_list.append({
                'id': restaurant.id,
                'name': restaurant.name,
                'image': restaurant.image_url,
                'name_restaurant': restaurant.name_restaurant,
                'description': restaurant.description,
                'direccion': restaurant.direccion
            })
        
        return jsonify(restaurants_list)
    else:
        response = jsonify({'message':'Unauthorized'})
        return response, 401