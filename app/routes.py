from flask import Flask, render_template, redirect, Blueprint, session, url_for, session
from app.models import db, Users
from flask_mail import Message
from flask import current_app as app
import random
from . import firebase as fb
from app.forms import LoginForm, RegisterForm, VerifyForm


main = Blueprint('main', __name__)
@main.route('/')
def land():
    return render_template('base.html')



@main.route('/about/<username>')
def about(username):
    users = [
        {'id':1, 'name' : 'Roal', 'email':'Royal@abcd.in' },
        {'id':2, 'name' : 'Royl', 'email':'Royal@acd.in' },
        {'id':3, 'name' : 'Royal', 'email':'Royal@abd.in' }
    ]
    return render_template('about.html', name=username, users=users)

@main.route('/firstpage')
def firstpage():
    user = session.get('user')
    return render_template('firstpage.html', user=user)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(password)
        print('try executed')
        user=fb.auth.sign_in_with_email_and_password(email, password)
        print('user fetched')
        info = fb.auth.get_account_info(user['idToken'])
        print('info fetched')
        email_verified = info['users'][0]['emailVerified']
        print('email verified')
        print(user)
        print(info)
        print(email_verified)
        if email_verified:
            print("email verified")
            session['user'] = email
            print('session created')
            return redirect(url_for('main.firstpage'))
        else:
            print("Email Not Verified")
            return "<h1>Please Verify Your Mail</h1>"
    return render_template("login.html", form=form)


@main.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = fb.auth.create_user_with_email_and_password(email, password)
        session['user'] = email
        print("Try block executed")
        fb.auth.send_email_verification(user['idToken'])
        print("Mail Sent")
        return redirect(url_for('main.login'))

    else:
        print("Form not validated")
    return render_template('register.html', form=form)
        

# @main.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         email = form.email.data
#         password = form.password.data
        
#         if not username or not email or not password:
#             print("All fields must be filled out.", "error")
#             return render_template('register.html', form=form)
        
#         sender = app.config.get('MAIL_USERNAME')  
        
#         if sender is None:
#             print("Mail sender is not configured.", "error")
#             return render_template('register.html', form=form)
        
#         otp = generateOTP()
         
#         msg = Message(subject='Verify Your Email',
#                   recipients=[email])
#         msg.body = f"This mail is for verification please enter the otp {otp} on the page"
#         try:
#             app.mail.send(msg)
#             print("Mail sent")
#             print(otp)
#             session['username'] = username
#             session['email'] = email
#             session['password'] = password
#             session['otp'] = otp
#             return redirect(url_for('main.verifyotp'))
#         except Exception as e:
#             print(f"Failed to send email: {e}", "error")
#             return render_template('register.html', form=form)
#     else:
#         print("Form not validated")
#     return render_template('register.html', form=form)


@main.route('/verifyotp1', methods=['GET', 'POST'])
def verifyotp():
    form = VerifyForm()
    if form.validate_on_submit():
        otp = session.get('otp')
        if otp is None:
            return "No OTP provided", 400 
        tocheckotp = form.otp.data
        print(tocheckotp)
        username = session.get('username')
        password = session.get('password')
        email = session.get('email')
        print(otp)
        if tocheckotp == otp:
            hashedpwd = app.extensions['bcrypt'].generate_password_hash(password).decode('utf-8')
            user_to_create = Users(username=username, email=email, password=hashedpwd, is_verified=True)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            print("False OTP")
    else:
        print("Form not validated")
    return render_template('verifyotp.html', form=form)

def generateOTP():
    digits = '0123456789'
    OTP = ''.join(random.choice(digits) for i in range(4))
    return OTP
