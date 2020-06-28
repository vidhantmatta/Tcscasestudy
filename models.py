from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient.db' 
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssnId = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    admissionDate = db.Column(db.String(10), nullable=False)
    bedType = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Active")
    
    def __repr__(self):
        return 'Patient' + str(self.id)