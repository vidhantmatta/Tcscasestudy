from flask import Flask, Blueprint, render_template, request, redirect
from models import Patient,db
from flask_sqlalchemy import SQLAlchemy
deskExec = Blueprint('deskExec',__name__,template_folder='./')



@deskExec.route('/home')
def index():
    allPatients = Patient.query.all()
    return render_template('deskExec/home.html', patients=allPatients)

@deskExec.route('/patients')
def patients():
    allPatients = Patient.query.all()
    return render_template('deskExec/patients.html', patients=allPatients)

@deskExec.route('/create', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        patient_ssnId = request.form['ssnId']
        patient_name = request.form['name']
        patient_age = request.form['age']
        patient_admissionDate = request.form['admissionDate']
        patient_bedType = request.form['bedType']
        patient_address = request.form['address']
        patient_city = request.form['city']
        patient_state = request.form['state']
        newPatient = Patient(ssnId=patient_ssnId, name=patient_name, age=patient_age, admissionDate=patient_admissionDate,
        bedType =patient_bedType, address=patient_address, city=patient_city, state=patient_state)
        db.session.add(newPatient)
        db.session.commit()
        return redirect('/patients')
    else:
        return render_template('deskExec/newPatient.html')


@deskExec.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':    
        searched_ssnId = request.form['ssnId']
        allPatients = Patient.query.all()
        for patient in allPatients:
            if(patient.ssnId == searched_ssnId):
                return render_template('deskExec/patientInfo.html', patient= patient)
        return redirect('/home')
    
@deskExec.route('/delete/<int:id>')
def delete(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect('/patients')

@deskExec.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.ssnId = request.form['ssnId']
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.admissionDate = request.form['admissionDate']
        patient.bedType = request.form['bedType']
        patient.address = request.form['address']
        patient.city = request.form['city']
        patient.state = request.form['state']
        db.session.commit()
        return redirect('/patients')
    else:
        return render_template('deskExec/update.html', patient=patient)