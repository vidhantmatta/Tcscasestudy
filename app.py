from flask import Flask, render_template, request, redirect, flash,url_for
from flask_sqlalchemy import SQLAlchemy
from views.deskExec import deskExec
from views.pharmacist import pharmacist
from models import Auth,Patient

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient.db'
db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template("login.html")


@app.route('/',methods=['POST'])
def loginauth():

    if request.method == 'POST':
        patient_username = request.form['username']
        patient_pass = request.form['password']
        alluser = Auth.query.all()
        for user in alluser:
            if(user.username == patient_username and user.password == patient_pass):
                if(user.role == "pharma"):
                    return redirect(url_for('pharmacist.allmedicines'))
                if(user.role == "deskExec"):
                    allPatients = Patient.query.all()
                    return render_template("/deskExec/home.html", patients= allPatients)

        return redirect("/")


#deskExecutive routes
app.register_blueprint(deskExec)

#pharmacy routes
app.register_blueprint(pharmacist)

#diagonistics routes


if __name__ == "__main__":
    app.secret_key='secret123'
    app.run(debug=True)
