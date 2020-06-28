from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from views.deskExec import deskExec

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patient.db' 
db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template("login.html")
    
    
#deskExecutive routes
app.register_blueprint(deskExec)

#pharmacy routes

#diagonistics routes


if __name__ == "__main__":
    app.run(debug=True)
