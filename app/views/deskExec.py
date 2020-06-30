from app import app,render_template, redirect, request, flash
from models import db, Patient
from flask_login import login_required, current_user

@app.route("/home")
@login_required
def index():
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')

    allPatients = Patient.query.all()
    return render_template('deskExec/home.html', patients=allPatients)

@app.route('/patients')
@login_required
def patients():
    allPatients = Patient.query.all()
    return render_template('deskExec/patients.html', patients=allPatients)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def new_post():
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')

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
        flash('Patient created')
        return redirect('/patients')
    else:
        return render_template('deskExec/newPatient.html')


@app.route('/search', methods=['POST'])
@login_required
def search():
    '''if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')'''

    if request.method == 'POST':    
        searched_ssnId = request.form['ssnId']
        patient = Patient.query.filter_by(ssnId=searched_ssnId).first()
        if not patient:
            flash('No patients found with given ssnID')
            if(current_user.role == 'desk'):
                return redirect('/home')
            elif(current_user.role == 'pharm'):
                return redirect('/pharmacist_dashboard')

        return render_template('deskExec/patientInfo.html', patient= patient)
        
        
    
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted')
    return redirect('/patients')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
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
        flash('Patient details updated')
        return redirect('/patients')
    else:
        return render_template('deskExec/update.html', patient=patient)

