from flask import render_template, url_for, flash, redirect
from pyblogger import app, db, bcrypt
from pyblogger.forms import RegistrationForm, LoginForm
from pyblogger.models import User, Post
from flask_login import login_user, current_user, logout_user
from pyblogger.data import posts



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        ### hashing the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ### creating user object to store it into the database
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        ### adding the user into the database
        db.session.add(user)
        ### commit those changes
        db.session.commit()
        flash(f'You Account has been created! You are now able to login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        ### checking if the user trying to login is in th database
        user = User.query.filter_by(email = form.email.data ).first()
        ### checking if user is present and its password matches the entered password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            ### logins the user, also remember me and duration functionality can be used
            login_user(user, remember= form.remember.data)
            ### flashing login success message on the redirected page
            flash(f'Welcome {user.username}', 'success')

            return redirect(url_for('home'))

        else:
            flash(f'Login Unsuccessful ! Please Check Email and Password...', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout" )
def logout():
    logout_user()
    return redirect(url_for('login'))
