from app import app, Flask, render_template, request, redirect,url_for,flash
from models import Patient,Patientdiagnostic,Diagnosistests,db
from flask_login import login_required, current_user


tempPatientTests = {}

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
        patient = Patient.query.filter_by(ssnId = search_ssnId).first()
        tests = Patientdiagnostic.query.filter_by(pid=patient.id).all()
        testsList=[]
        # TODO: Get the temporary list after the add function is executed and pass it below
        tempTests = tempPatientTests
        for test in tests:
            testsList.append(Diagnosistests.query.filter_by(test_id=test.dtest_id).all())
        print(testsList)
        allPatients = Patient.query.all()
        return render_template('diagnostic/searchPatientDiagnostic.html', patient=patient, diagnosis=zip(tests, testsList),
                                       patients=allPatients, dTestDict = tempTests)

        return redirect('/diagnostic_dashboard')

# This is to add the test to the temporary list when "Add Diagnosis" is pressed
@app.route('/add_test/<int:ssn_id>', methods=['GET', 'POST'])
@login_required
def new_test(ssn_id):
    if(current_user.role != 'diag'):
        return render_template('auth/accessDenied.html')
    if request.method == 'POST':
            test_name= request.form['tName']
            test_rate = request.form['tRate']
            patient = Patient.query.filter_by(ssnId = ssn_id).first()
            print("ssn id is: " + ssn_id)
            print("name is : " + patient.id)
            # To verify that the Test is not already added in the temporary list
            if test_name not in tempPatientTests:
                print('Received values from form: ' +test_name + ' ' + test_rate)
                tempPatientTests[test_name] = test_rate
                print(tempPatientTests[test_name])
                flash("New Test added","success")
                # We need to pass the dictionary value here below for the temporary list to work
                return redirect('/diagnostic', patient=patient, dTestDict = tempPatientTests ) 
                # TODO: The upper logic doesnt seem to work. Need to Work on a fix
            else:
                flash("Test already exist","danger")
                return render_template('diagnostic/new_test.html')
    else:
        return render_template('diagnostic/new_test.html')

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