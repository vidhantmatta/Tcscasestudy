from app import app, render_template, request, redirect, url_for,flash
from models import Patient,Med,Pmed,db
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

newMed = []

@app.route('/pharmacist_dashboard')
@login_required
def pharm():
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    allPatients = Patient.query.all()
    return render_template('pharmacist/searchpatient.html', patients=allPatients)


@app.route('/pharmacist', methods=['GET','POST'])
def pharmacistinfo():
    if (current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        search_ssnId = request.form['ssnId']
        try:
            searched_ssnId = int(search_ssnId)
        except:
            flash("Please Enter a valid Integer Id!" , "danger")
            return redirect('/pharmacist_dashboard')
        return redirect(url_for('patientmedinfo',ssn=searched_ssnId))


@app.route('/pharmacist/<int:ssn>', methods=['GET', 'POST'])
@login_required
def patientmedinfo(ssn):
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    patient = Patient.query.filter_by(ssnId = ssn).first()
    medicine = Pmed.query.filter_by(pid=patient.id).all()
    patientmedlist=[]
    for med in medicine:
        patmedDict = {}
        issuedMed = Med.query.filter_by(mid=med.medicineId)[0]
        patmedDict['name'] = issuedMed.mname
        patmedDict['quantity'] = med.quant
        patmedDict['rate'] = issuedMed.Rate
        patmedDict['amount'] = med.amount

        patientmedlist.append(patmedDict)
    allPatients = Patient.query.all()
    return render_template('pharmacist/searchpatient.html', ssn=ssn, newMed=newMed, patient= patient,medicine= patientmedlist,patients=allPatients)
    #
    # return redirect('/pharmacist_dashboard')

@app.route('/add_medicine', methods=['GET', 'POST'])
@login_required
def new_medi():
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        try:
            medicine_name= request.form['mname']
            medicine_quantity = request.form['quantity']
            medicine_rate = request.form['Rate']
            newMedicine = Med(mname=medicine_name,quantity=medicine_quantity,Rate=medicine_rate)
            db.session.add(newMedicine)
            db.session.commit()
            flash("New medicine added","success")
            return redirect('/all_medicines')
        except IntegrityError:
            db.session.rollback()
            flash("Medicine already exist","danger")
            return render_template('pharmacist/new_medicine.html')
    else:
        return render_template('pharmacist/new_medicine.html')

@app.route('/all_medicines')
@login_required
def allmedicines():
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    medicines=Med.query.all()
    return render_template('pharmacist/medicines.html', medicines=medicines)

@app.route('/issuemedicine/<int:ssn>', methods=['GET','POST'])
@login_required
def issuemedicine(ssn):
    if (current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    allMeds = Med.query.all()
    return render_template('pharmacist/issuemedicine.html', meds=allMeds,ssn=ssn)

@app.route('/addnewmed/<int:ssn>', methods=['GET','POST'])
@login_required
def addnewmed(ssn):
    if (current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    if request.method == "POST":
        medName = request.form['mname']
        reqQuant = request.form['quantity']
        requiredMed= Med.query.filter_by(mname = medName)[0]
        patId = Patient.query.filter_by(ssnId = ssn)[0].id
        if (int(requiredMed.quantity) - int(reqQuant))>=0:
            medDict={}
            medDict['medId'] = requiredMed.mid
            medDict['pid'] = patId
            medDict['name'] = medName
            medDict['quant'] = reqQuant
            medDict['rate'] = requiredMed.Rate
            medDict['amount'] = int(reqQuant) * int(requiredMed.Rate)
            newMed.append(medDict)
            print(medDict['name'])
            return redirect(url_for('patientmedinfo',ssn=ssn))

        else:
            flash("Quantity not availaible. Available quantity of this medicine is {}".format(requiredMed.quantity), "danger")
            return redirect(url_for('issuemedicine', ssn=ssn))

@app.route('/updatelist/<int:ssn>', methods=['GET','POST'])
@login_required
def updatemedlist(ssn):
    if (current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    for med in newMed:
        quantity_med = Med.query.get(med['medId'])
        quantity_med.quantity = int(quantity_med.quantity)-int(med['quant'])
        db.session.commit()
        obj = Pmed(pid=med['pid'],medicineId=med['medId'],quant=med['quant'],amount=med['amount'])
        db.session.add(obj)
        db.session.commit()
    newMed.clear()
    return redirect(url_for('patientmedinfo',ssn=ssn))



