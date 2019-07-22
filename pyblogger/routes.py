import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from pyblogger import app, db, bcrypt
from pyblogger.forms import RegistrationForm, LoginForm, UpdateAccountForm
from pyblogger.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
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
        user = User.query.filter_by(email=form.email.data).first()
        ### checking if user is present and its password matches the entered password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            ### logins the user, also remember me and duration functionality can be used
            login_user(user, remember=form.remember.data)
            ### redirects the user to account page if the query is present in the url box
            next_page = request.args.get('next')
            ### flashing login success message on the redirected page
            flash(f'Welcome {user.username}', 'success')

            return redirect(next_page) if next_page else redirect(url_for('home'))

        else:
            flash(f'Login Unsuccessful ! Please Check Email and Password...', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    ### create UpdateAccountForm instance
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Your account has been updated!', 'success')

        ###---------------------------------VIMP-----------------------------------------
        ### you want to follow post get redirect pattern here, because if you render template
        ### i.e. if you do not redirect, it will refresh the page, and you will see a
        ### CONFIRM FORM RESUBMISSION pop up. which is weird.
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
# GU
