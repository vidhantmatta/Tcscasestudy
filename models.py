from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy import event



app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient.db'
db = SQLAlchemy(app)


class Auth(db.Model):
    aid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return 'User' + str(self.aid)

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


class Med(db.Model):
    mid = db.Column(db.Integer,primary_key=True)
    mname = db.Column(db.String(150), nullable = False , unique=True)
    quantity = db.Column(db.String(150), nullable = False)
    Rate = db.Column(db.Integer, nullable = False)



class Pmed(db.Model):
    pid = db.Column(db.Integer,db.ForeignKey('patient.id'),primary_key=True)
    medicineId = db.Column(db.Integer,db.ForeignKey('med.mid'), nullable = False)
    quant = db.Column(db.String(150), nullable = False)
    amount = db.Column(db.Integer ,nullable=False)
    issueDate = db.Column(db.DateTime, default=datetime.now)
    patient = db.relationship("Patient", backref=backref('patients') )
    med = db.relationship("Med", backref=backref('medicines') )

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
