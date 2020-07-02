from app import app,render_template, redirect, request, flash
from models import db, Patient, Med, Pmed, Diagnosistests, Patientdiagnostic, History
from datetime import datetime
from flask_login import login_required, current_user



# This block of code is used to render details of a particular active patient in the hospital..
@app.route("/home")
@login_required
def index():
    #Checks if user is Desk Executive. If not,deny access to further pages.
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')
    allPatients = Patient.query.all()
    return render_template('deskExec/home.html', patients=allPatients)




"""
 This block of code is used to render list of active patients to the admission
 desk executive in the hospital..
"""
@app.route('/patients')
@login_required
def patients():
    allPatients = Patient.query.all()
    return render_template('deskExec/patients.html', patients=allPatients)




# This route adds new patient along with his details in the hospital database using a form.
@app.route('/create', methods=['GET', 'POST'])
@login_required
def new_patient():
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')
    #When form is submitted
    if request.method == 'POST':
        # rendering form data and adding to the database
        patient_ssnId = request.form['ssnId']
        patient_name = request.form['name']
        patient_age = request.form['age']
        patient_admissionDate = request.form['admissionDate']
        patient_bedType = request.form['bedType']
        patient_address = request.form['address']
        patient_city = request.form['city']
        patient_state = request.form['state']
        if(not len(patient_ssnId)==9 or not patient_ssnId.isdigit()):
            flash("ssnId must be a 9 digit number" , "danger")
            return render_template("deskExec/newPatient.html", patient_ssnId=patient_ssnId,patient_name=patient_name,patient_age=patient_age,
            patient_admissionDate=patient_admissionDate, patient_city=patient_city,patient_state=patient_state)


#********************VALIDATIONS*******************************************

        # Alloting unique ssnId to each patient
        if(Patient.query.filter_by(ssnId=patient_ssnId).first()):
            flash("Patient with the same ssnId already exists in the database" , "danger")
            return redirect('/home')

        # Checking if any form field is empty
        if(len(patient_name)==0 or len(str(patient_age))==0 or len(patient_admissionDate)==0 or len(patient_bedType)==0
        or len(patient_address)==0 or len(patient_city)==0 or len(patient_state)==0):
            flash("No field must be empty" , "danger")
            return render_template("deskExec/newPatient.html", patient_ssnId=patient_ssnId,patient_name=patient_name,patient_age=patient_age,
            patient_admissionDate=patient_admissionDate, patient_city=patient_city,patient_state=patient_state)

#*********************************************************************************

        newPatient = Patient(ssnId=patient_ssnId, name=patient_name, age=patient_age, admissionDate=patient_admissionDate,
        bedType =patient_bedType, address=patient_address, city=patient_city, state=patient_state)
        db.session.add(newPatient)
        db.session.commit()
        flash('Patient created','success')
        return redirect('/patients')
    else:
        return render_template('deskExec/newPatient.html')



"""
This block of code is used to search a patient using its "ssnId" in order to get
all the information about him.
"""
@app.route('/search', methods=['POST'])
@login_required
def search():
    '''if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')'''

    if request.method == 'POST':
        searched_ssnId = request.form['ssnId']
        patient = Patient.query.filter_by(ssnId=searched_ssnId).first()
        if not patient:
            flash('No patients found with given ssnID','danger')
            if(current_user.role == 'desk'):
                return redirect('/home')
            elif(current_user.role == 'pharm'):
                return redirect('/pharmacist_dashboard')

        return render_template('deskExec/patientInfo.html', patient= patient)




# This route is used to delete patient's data from the hospital's database
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted','success')
    return redirect('/patients')



# This route is used to update patient's details in the hospital database.
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        patient_name = request.form['name']
        patient_age = request.form['age']
        patient_admissionDate = request.form['admissionDate']
        patient_bedType = request.form['bedType']
        patient_address = request.form['address']
        patient_city = request.form['city']
        patient_state = request.form['state']
        #VALIDATIONS******************
        if(len(patient_name)==0 or len(str(patient_age))==0 or len(patient_admissionDate)==0 or len(patient_bedType)==0
        or len(patient_address)==0 or len(patient_city)==0 or len(patient_state)==0):
            flash("No field must be empty" , "danger")
            return render_template('deskExec/update.html', patient=patient)
        patient.name = patient_name
        patient.age = patient_age
        patient.admissionDate = patient_admissionDate
        patient.bedType = patient_bedType
        patient.address = patient_address
        patient.city = patient_city
        patient.state = patient_state
        db.session.commit()
        flash('Patient details updated','success')
        return redirect('/patients')
    else:
        return render_template('deskExec/update.html', patient=patient)




# This function generates a bill for patient with the total amount of services provided to the patient....
@app.route('/generateBill/<int:id>')
@login_required
def generateBill(id):
    patient = Patient.query.get_or_404(id)
    medicines = Pmed.query.filter_by(pid=patient.id).all()
    tests = Patientdiagnostic.query.filter_by(pid=patient.id).all()

    medAmount=0
    roomCharge=0
    testAmount=0

    for med in medicines:
        medAmount+=med.amount

    for test in tests:
        testAmount+=test.amount

    if(patient.bedType == "General Ward"):
        roomCharge = 500
    elif(patient.bedType == "Semi Sharing"):
        roomCharge = 1000
    else:
        roomCharge = 2000

    #Grand total of amount of services offered to the patient.
    total = medAmount + roomCharge + testAmount

    return render_template('deskExec/generateBill.html', patient=patient, medicines = medicines, tests = tests,
    medAmount=medAmount, roomCharge=roomCharge, testAmount=testAmount, total=total)



"""
This block of code renders all the details of services provided to the patient,
adds his data to the history table and then changes patient's status to "Discharged".....
"""
@app.route("/discharge/<int:id>")
@login_required
def discharge(id):
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')

    patient = Patient.query.get_or_404(id)
    medicines = Pmed.query.filter_by(pid=patient.id).all()
    tests = Patientdiagnostic.query.filter_by(pid=patient.id).all()

    patientDoj = patient.admissionDate.split("/")
    currDate = str(datetime.now())[:10].split("-")
    diff = datetime(int(currDate[0]),int(currDate[1]),int(currDate[2]))-datetime(int(patientDoj[0]),int(patientDoj[1]),int(patientDoj[2]))
    activeDays = str(diff).split(",")[0]

    #adding history to the patient's previous history
    hid = id
    Tests = ""
    Meds = ""
    for test in tests:
        Tests += ", " + test.diagnosistests.test_name
    for med in medicines:
        Meds += ", " + med.med.mname

    hTests = Tests[1:]
    hMeds = Meds[1:]

    newHistory = History(hid=hid, tests=hTests, medicines=hMeds, activeDays=activeDays, dischargeDate=str(datetime.now())[:10])
    db.session.add(newHistory)
    db.session.commit()

    #deleting medicines for current session after discharge
    for medicine in medicines:
        db.session.delete(medicine)

    #deleting tests for current session after discharge
    for test in tests:
        db.session.delete(test)

    patient.status = "Discharged"
    db.session.commit()

    flash('Patient discharged','success')
    return redirect('/patients')



# This route is used to find out patient's history......
@app.route("/history/<int:id>")
@login_required
def history(id):
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')

    patient = Patient.query.get_or_404(id)
    histories = History.query.filter_by(hid=id).all()
    histories.reverse()
    return render_template("deskExec/history.html", histories = histories, patient = patient)




# This route is use to re-active the patient if he gets admitted again and change hihs status to "active"...
@app.route("/reactivate/<int:id>")
@login_required
def reactivate(id):
    if(current_user.role != 'desk'):
        return render_template('auth/accessDenied.html')

    patient = Patient.query.get_or_404(id)
    patient.admissionDate = str(datetime.now())[:10]
    patient.status = "Active"
    db.session.commit()

    flash('Patient status activated','success')
    return redirect('/patients')
