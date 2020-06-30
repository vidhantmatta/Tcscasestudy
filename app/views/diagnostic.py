from app import app, Flask, render_template, request, redirect,url_for,flash
from models import Patient,Patientdiagnostic,Diagnosistests,db
from flask_login import login_required, current_user



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
        for test in tests:
            testsList.append(Diagnosistests.query.filter_by(test_id=test.dtest_id).all())
        print(testsList)
        allPatients = Patient.query.all()
        return render_template('diagnostic/searchPatientDiagnostic.html', patient=patient, diagnosis=zip(tests, testsList),
                                       patients=allPatients)

        return redirect('/diagnostic_dashboard')
