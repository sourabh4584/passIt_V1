from flask import Blueprint , render_template , redirect , url_for , flash , request
from werkzeug.security import generate_password_hash , check_password_hash
from .models import User
from . import db
from flask_login import login_user , logout_user , login_required
from .sup_func import validation_pin

auth = Blueprint('auth' , __name__)

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    user = User.query.filter_by(email = email).first()
    if not user or not check_password_hash(user.password , password):
        flash('Login details are Incorrect. Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember )
    return redirect(url_for('auth.pin_confirm'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return "<H1><center> YOU ARE LOGGED OUT OF THE ACCOUNT... </center></H1>"

@auth.route('/pin')
@login_required
def pin_confirm():
    return render_template('pincode.html')

@auth.route('/pin' , methods=['POST'])
def post_pin_confirm():
    # code connecting to the database
    pwd = request.form.get('pwd1')
    if (len(str(pwd)) != 6):
        flash('Password must contain 6 digits')
        return redirect(url_for('auth.pin_confirm'))
 
    try:
        val = int(pwd)
    except Exception as ValueError:
        flash('Password must contain DIGITS/NUMBERS[0-9] only')
        return redirect(url_for('auth.pin_confirm'))

    # writing in database now
    i = db.session.query(User).filter(User.email.ilike('sourabhmishra1262@gmail.com')).update({"pin": pwd}, synchronize_session='fetch' ) 
    # db.session.add(User(pin = pwd))
    db.session.commit( )
    return redirect(url_for('main.profile'))
