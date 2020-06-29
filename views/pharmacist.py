from flask import Flask, Blueprint, render_template, request, redirect,url_for,flash
from models import Patient,Med,Pmed,db
from flask_sqlalchemy import SQLAlchemy
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
            print("please enter an intefer")
            return redirect('/pharmacist_dashboard')
        print(type(searched_ssnId))
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
