from app import app, db
from flask_login import current_user, login_required, login_user, logout_user
from flask import url_for, redirect, render_template, flash
from app.forms import LoginForm, RegistrationForm
from app.models import User, requires_roles


@app.route('/', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('customer'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('Invalid username')
            return redirect(url_for('signin'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('customer'))
    return render_template('signin.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        user = User(username=username, email=email, role=role);
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('signin'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/customer')
@login_required
@requires_roles('admin', 'customer')
def customer():
    return render_template('userprofile.html', title="User Profile")


@app.route('/admin')
@login_required
@requires_roles('admin')
def admin():
    return render_template('userprofile.html', title="Admin Profile")


@app.route('/logout')
@login_required
@requires_roles('admin','customer')
def logout():
    logout_user()
    return redirect(url_for('signin'))
