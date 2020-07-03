from app import app,render_template, redirect, request, flash, url_for
from models import db, Patient, User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, current_user, logout_user


# Basic route to render login form for the user.......
@app.route('/')
def senduser():
    return render_template('auth/login.html')



# Route to register login credentials for the hospital staff......
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(username=username).first()

        if user:
            flash('user already exists!','danger')
            return redirect('/signup')

        newUser = User(username=username,
        password=generate_password_hash(password, method='sha256'),
        role=role)
        db.session.add(newUser)
        db.session.commit()

        # Use of flash to show appropriate messages....
        flash('user created.','success')
        return redirect('/signup')
    else:
        return render_template('auth/signup.html')



# This block takes login credentials from the user, verify it and redirect the user according to his role..
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()
        if not user:
            flash('Wrong username!','danger')
            return redirect('login')
        elif not check_password_hash(user.password,password):
            flash('Password incorrect!','danger')
            return redirect('login')

        login_user(user)


        #Checks if user's role is desk executive
        if current_user.role == 'desk':
            flash('Welcome, '+ current_user.username + '!','success')
            return redirect('/home')

        #Checks if user's role is pharmacist
        elif current_user.role == 'pharm':
            flash('Welcome, '+ current_user.username + '!', 'success')
            return redirect('/pharmacist_dashboard')

        #Checks if user's role is diagnostic service executive
        elif current_user.role == 'diag':
            flash('Welcome, '+ current_user.username + '!', 'success')
            return redirect('/diagnostic_dashboard')

        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')



# Route for logout functionality......
@app.route('/logout')
# decorator to ensure that user is logged in.....
@login_required
def logout():
    logout_user()
    flash('successfully logged out!','success')
    return redirect('/login')
