from flask_login import UserMixin
from app import db
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy import event


"""
Model to create a database table for storing login credentials for all hospital staff
with their roles.......
"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)



# Model to create database table for storing all the relevant patients' details......
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



"""
Model to create database table for storing all the details of medicine along with
its quantity and rate....
"""
class Med(db.Model):
    mid = db.Column(db.Integer,primary_key=True)
    mname = db.Column(db.String(150), nullable = False , unique=True)
    quantity = db.Column(db.String(150), nullable = False)
    Rate = db.Column(db.Integer, nullable = False)



# Model to create database table for storing patient's drug information.......
class Pmed(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer,db.ForeignKey('patient.id'))
    medicineId = db.Column(db.Integer,db.ForeignKey('med.mid'), nullable = False)
    quant = db.Column(db.String(150), nullable = False)
    amount = db.Column(db.Integer ,nullable=False)
    issueDate = db.Column(db.DateTime, default=datetime.now)
    patient = db.relationship("Patient", backref=backref('patients'))
    med = db.relationship("Med", backref=backref('medicines'))




# Model to create database table for storing all the details of tests.......
class Diagnosistests(db.Model):
    test_id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(150), nullable=False, unique=True)
    rate = db.Column(db.Integer, nullable=False)



# Model to create database table for storing patient's tests information.......
class Patientdiagnostic(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('patient.id'))
    dtest_id = db.Column(db.Integer, db.ForeignKey('diagnosistests.test_id'), nullable = False)
    amount = db.Column(db.Integer, nullable=False)
    issueDate = db.Column(db.DateTime, default=datetime.now)
    patient = db.relationship("Patient", backref=backref('diagpatients'))
    diagnosistests = db.relationship("Diagnosistests", backref=backref('diagnosistests'))



# Model to create database table to store all the details of medical services rendered to the patient...
class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    hid = db.Column(db.Integer,db.ForeignKey('patient.id'))
    tests = db.Column(db.String(150), nullable = True)
    medicines = db.Column(db.String(150), nullable = True)
    dischargeDate = db.Column(db.String(10), nullable=False)
    activeDays = db.Column(db.String(15), nullable = False)



# function to make foreign_keys connection....
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
