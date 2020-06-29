from flask import Flask, Blueprint, render_template, request, redirect,url_for,flash
from models import Patient,Med,Pmed,db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
pharmacist = Blueprint('pharmacist',__name__,template_folder='./')



@pharmacist.route('/pharmacist_dashboard')
def pharm():
    allPatients = Patient.query.all()
    return render_template('pharmacist/searchpatient.html', patients=allPatients)


@pharmacist.route('/pharmacist', methods=['GET','POST'])
def pharmacistinfo():
    if request.method == 'POST':
        search_ssnId = request.form['ssnId']
        try:
            searched_ssnId = int(search_ssnId)
        except:
            flash("Please Enter a valid Integer Id!" , "danger")
            return redirect('/pharmacist_dashboard')
        allPatients = Patient.query.all()
        for patient in allPatients:
            if(patient.ssnId == searched_ssnId):
                medicine = Pmed.query.filter_by(pid=patient.id).all()
                medi=[]
                for med in medicine:
                    medi.append(Med.query.filter_by(mid=med.medicineId).all())
                print(medi)
                return render_template('pharmacist/searchpatient.html', patient= patient,medicine= zip(medicine,medi),patients=allPatients)

        return redirect('/pharmacist_dashboard')

@pharmacist.route('/add_medicine', methods=['GET', 'POST'])
def new_medi():
    if request.method == 'POST':
        try:
            medicine_name= request.form['mname']
            medicine_quantity = request.form['quantity']
            medicine_rate = request.form['Rate']
            newMedicine = Med(mname=medicine_name,quantity=medicine_quantity,Rate=medicine_rate)
            db.session.add(newMedicine)
            db.session.commit()
            flash("New medicine added","success")
            return redirect('/pharmacist_dashboard')
        except IntegrityError:
            db.session.rollback()
            flash("Medicine already exist","danger")
            return render_template('pharmacist/new_medicine.html')
    else:
        return render_template('pharmacist/new_medicine.html')

@pharmacist.route('/all_medicines')
def allmedicines():
    medicines=Med.query.all()
    return render_template('pharmacist/medicines.html', medicines=medicines)
