from flask import Flask, Blueprint, render_template, request, redirect,url_for,flash
from models import Patient,PatientDiagnostic,DiagnosisTests,db
from flask_sqlalchemy import SQLAlchemy
diagnostic = Blueprint('diagnostic',__name__,template_folder='./')



@diagnostic.route('/diagnostic_dashboard')
def diag():
    allPatients = Patient.query.all()
    return render_template('diagnostic/searchPatientDiagnostic.html', patients=allPatients)


@diagnostic.route('/diagnostic', methods=['GET','POST'])
def diagnosticinfo():
    if request.method == 'POST':
        search_ssnId = request.form['ssnId']
        try:
            searched_ssnId = int(search_ssnId)
        except:
            flash("Please Enter a valid Integer Id!", "danger")
            print("please enter an integer")
            return redirect('/diagnostic_dashboard')
        print(type(searched_ssnId))
        allPatients = Patient.query.all()
        for patient in allPatients:
            if patient.ssnId == searched_ssnId :
                tests = PatientDiagnostic.query.filter_by(pid=patient.id).all()
                testsList=[]
                for test in tests:
                    testsList.append(DiagnosisTests.query.filter_by(test_id=test.dtest_id).all())
                print(testsList)
                return render_template('diagnostic/searchPatientDiagnostic.html', patient=patient, diagnosis=zip(tests, testsList),
                                       patients=allPatients)

        return redirect('/diagnostic_dashboard')
