from flask import render_template,redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import User
from datetime import datetime
from .forms import LoginForm, RegistrationForm,ChangePasswordForm,ChangeEmailForm
from  ..models import db
from ..email import send_email
from flask_login import current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next')or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html',current_time=datetime.utcnow(),form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email= form.email.data, password =form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to your email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',current_time=datetime.utcnow(),form=form)

@auth.route('/change_email',methods=['GET','POST'])
@login_required
def change_email_request():
    form=ChangeEmailForm
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address','auth/email/change_email',user=current_user, token=token)
            flash("An email with instructions to confirm your new email address has been sent to you")
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)        

@auth.route('/change-password', methods=['GET','POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password =form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash ('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password,')
    return render_template("auth/change_password.html", form=form)        
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/secret')
@login_required
def  secret():
    return 'only authenticated users allowed!'


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html',current_time=datetime.utcnow() )

    
@auth.route('/resend_confirm')
@login_required
def resend_confirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email')

    return redirect(url_for('main.index'))





