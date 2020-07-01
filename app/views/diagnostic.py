from app import app, Flask, render_template, request, redirect,url_for,flash
from models import Patient,Patientdiagnostic,Diagnosistests,db
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError


tempPatientTests = []

@app.route('/diagnostic_dashboard')
@login_required
def diag():
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    allPatients = Patient.query.all()
    return render_template('diagnostic/searchPatientDiagnostic.html', patients=allPatients)

@app.route('/diagnostic', methods=['GET','POST'])
@login_required
def diagnosticinfo():
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        search_ssnId = request.form['ssnId']
        try:
            searched_ssnId = int(search_ssnId)
        except:
            flash("Please Enter a valid Integer Id!", "danger")
            print("please enter an integer")
            return redirect('/diagnostic_dashboard')
        return redirect(url_for('patienttestinfo', ssn=searched_ssnId))

@app.route('/diagnostic/<int:ssn>', methods=['GET', 'POST'])
@login_required
def patienttestinfo(ssn):
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    patient = Patient.query.filter_by(ssnId=ssn).first()
    tests = Patientdiagnostic.query.filter_by(pid=patient.id).all()
    testsList = []
    for test in tests:
        tempTest = {}
        name = Diagnosistests.query.filter_by(test_id=test.dtest_id)[0].test_name
        tempTest[name] = Diagnosistests.query.filter_by(test_id=test.dtest_id)[0].rate
        testsList.append(tempTest)
    print("Test list has: ")
    print(testsList)
    allPatients = Patient.query.all()
    return render_template('diagnostic/searchPatientDiagnostic.html',ssn = ssn, dTestList = tempPatientTests, patient=patient, diagnosis=testsList,
                           patients=allPatients)

@app.route('/issuetest/<int:ssn>', methods=['GET','POST'])
@login_required
def issuetest(ssn):
    if current_user.role != 'diag':
        return render_template('auth/accessDenied.html')
    allTests = Diagnosistests.query.all()
    return render_template('diagnostic/new_test.html', tests=allTests, ssn=ssn)

# This is to add the test to the temporary list when "Add Diagnosis" is pressed
@app.route('/add_test/<int:ssn>', methods=['GET', 'POST'])
@login_required
def new_test(ssn):
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        test_name= request.form['test_name']
        requiredTest = Diagnosistests.query.filter_by(test_name=test_name)[0]
        patient = Patient.query.filter_by(ssnId = ssn).first()
        # To verify that the Test is not already added in the temporary list
        testDict = {}
        testDict['testId'] = requiredTest.test_id
        testDict['pid'] = patient.id
        testDict['name'] = test_name
        testDict['rate'] = requiredTest.rate
        tempPatientTests.append(testDict)
        print(testDict['name'])
        return redirect(url_for('patienttestinfo', ssn=ssn))

@app.route('/updatetest/<int:ssn>', methods=['GET','POST'])
@login_required
def updateTestList(ssn):
    if (current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    for test in tempPatientTests:
        newTest = Patientdiagnostic(pid=test['pid'], dtest_id=test['testId'], amount = test['rate'])
        db.session.add(newTest)
        db.session.commit()
    tempPatientTests.clear()
    return redirect(url_for('patienttestinfo',ssn=ssn))

# Endpoint to display all the diagnosis tests available in the hospital
@app.route('/all_tests')
@login_required
def alltests():
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    dTestsList = Diagnosistests.query.all()
    return render_template('diagnostic/tests.html', dTestList=dTestsList)

# ********** EXTRA UTILITY FUNCTION ********** 

# This route is intended to just add new tests into the database.
@app.route('/add_diagdb', methods=['GET', 'POST'])
@login_required
def new_diagDB():
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
        try:
            test_name= request.form['tName']
            test_rate = request.form['tRate']
            print('Received values: ' +test_name + ' ' + test_rate)
            newTest = Diagnosistests(test_name=test_name,rate=test_rate)
            db.session.add(newTest)
            db.session.commit()
            flash("New Test added","success")
            return redirect('/all_tests')
        except IntegrityError:
            db.session.rollback()
            flash("Test already exist","danger")
            return render_template('diagnostic/addTestDB.html')
    else:
        return render_template('diagnostic/addTestDB.html')