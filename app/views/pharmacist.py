from app import app, render_template, request, redirect, url_for,flash
from models import Patient,Med,Pmed,db
from flask_login import login_required, current_user

@app.route('/pharmacist_dashboard')
@login_required
def pharm():
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    allPatients = Patient.query.all()
    return render_template('pharmacist/searchpatient.html', patients=allPatients)


@app.route('/pharmacist', methods=['GET','POST'])
@login_required
def pharmacistinfo():
    if(current_user.role != 'pharm'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        search_ssnId = request.form['ssnId']
        try:
            searched_ssnId = int(search_ssnId)
        except:
            flash("Please Enter a valid Integer Id!" , "danger")
            return redirect('/pharmacist_dashboard')
        patient = Patient.query.filter_by(ssnId = search_ssnId).first()
        medicine = Pmed.query.filter_by(pid=patient.id).all()
        medi=[]
        for med in medicine:
            medi.append(Med.query.filter_by(mid=med.medicineId).all())
        print(medi)
        allPatients = Patient.query.all()
        return render_template('pharmacist/searchpatient.html', patient= patient,medicine= zip(medicine,medi),patients=allPatients)

        return redirect('/pharmacist_dashboard')

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
            return redirect('/pharmacist_dashboard')
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
