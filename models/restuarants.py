from utils.db import db

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(400), nullable=False)
    name_department = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    contacto= db.Column(db.Text, nullable=False)

    def __init__(self, name, email, password,image_url,name_department, description, contacto):
        self.name = name
        self.email = email
        self.name_department = name_department
        self.password = password
        self.image_url = image_url
        self.description = description
        self.contacto = contacto