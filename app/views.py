from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Hobbies, Interests
from app.forms import ChooseForm, LoginForm, RegisterForm, AddHobbiesAndInterestsForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
import csv
import io
import datetime


@app.route("/")
def home():
    return render_template('home.html', title="Home")


# @app.route("/account")
# @login_required
# def account():
#     return render_template('account.html', title="Account")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('generic_form.html', title='Sign In', form=form)

@app.route('/student_profile/<int:studentID>', methods=['GET', 'POST'])
@login_required
def student_profile(studentID):
    form = AddHobbiesAndInterestsForm()
    choose_form = ChooseForm()
    q = db.select(User).where(User.id == studentID)
    student = db.session.scalars(q)

    q_hobby = db.select(Hobbies).where(Hobbies.user_id == studentID)
    student_hobby = db.session.scalars(q_hobby)

    hobbies_list = []
    for hobby in student_hobby:
        hobbies_list.append(hobby.hobbies)

    q_interest = db.select(Interests).where(Interests.user_id == studentID)
    student_interest = db.session.scalars(q_interest)

    interests_list = []
    for interest in student_interest:
        interests_list.append(interest.interests)

    if form.validate_on_submit():
        for each_hobby in form.hobbies.data:
            hobby = Hobbies(hobbies=each_hobby.strip(), user_id=current_user.id)
            db.session.add(hobby)

        for each_interest in form.interests.data:
            interest = Interests(interests=each_interest.strip(), user_id=current_user.id)
            db.session.add(interest)

        db.session.commit()

        flash('Hobbies and Interests added, successfully!', 'success')
        return redirect(url_for('student_profile', studentID=current_user.id))
    return render_template('student_profile.html', title='Student Profile', form=form, student=student, choose_form=choose_form, student_id=str(studentID), hobbies_list=hobbies_list, interests_list=interests_list)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, role=form.role.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

# Error handlers
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

# Error handler for 403 Forbidden
@app.errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Error'), 403

# Handler for 404 Not Found
@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Error'), 404

@app.errorhandler(413)
def error_413(error):
    return render_template('errors/413.html', title='Error'), 413

# 500 Internal Server Error
@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Error'), 500