from flask import render_template, redirect, url_for, flash, request, send_file, send_from_directory
from app import app
from app.models import User, Hobbies, Interests, Meeting
from app.forms import ChooseForm, LoginForm, RegisterForm, AddHobbiesAndInterestsForm, EditPersonalDetailsForm, MeetingForm
from flask_login import current_user, login_user, logout_user, login_required, fresh_login_required
import sqlalchemy as sa
from app import db
from urllib.parse import urlsplit
from app.models import Event
from app.forms import EventForm
from datetime import datetime
import csv
import io



@app.route("/")
def home():
    return render_template('home.html', title="Home")

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
    edit_form = EditPersonalDetailsForm()

    q = db.select(User).where(User.id == studentID)
    student = db.session.scalars(q)

    q_hobby = db.select(Hobbies).where(Hobbies.user_id == studentID)
    student_hobby = db.session.scalars(q_hobby)

    hobbies_list = []
    for hobby in student_hobby:
        each_hobby = []
        each_hobby.append(hobby.id)
        each_hobby.append(hobby.hobbies)
        hobbies_list.append(each_hobby)

    q_interest = db.select(Interests).where(Interests.user_id == studentID)
    student_interest = db.session.scalars(q_interest)

    interests_list = []
    for interest in student_interest:
        each_interest = []
        each_interest.append(interest.id)
        each_interest.append(interest.interests)
        interests_list.append(each_interest)

    #Adding Hobbies/Interests
    if form.validate_on_submit():
        new_hobby_added = False
        hobby_exists = False

        existing_hobbies = []
        for hobby in current_user.hobbies:
            existing_hobbies.append(hobby.hobbies)

        for each_hobby in form.hobbies.data:
            if each_hobby not in existing_hobbies:
                hobby = Hobbies(hobbies=each_hobby.strip(), user_id=current_user.id)
                db.session.add(hobby)
                new_hobby_added = True
            else:
                hobby_exists = True

        if new_hobby_added:
            flash('Hobbies added successfully!', 'info')
        if hobby_exists:
            flash('Hobbies already exists!', 'danger')

        new_interest_added = False
        interest_exists = False

        existing_interests = []
        for interest in current_user.interests:
            existing_interests.append(interest.interests)

        for each_interest in form.interests.data:
            if each_interest not in existing_interests:
                interest = Interests(interests=each_interest.strip(), user_id=current_user.id)
                db.session.add(interest)
                new_interest_added = True
            else:
                interest_exists = True

        if new_interest_added:
            flash('Interests added successfully!', 'info')
        if interest_exists:
            flash('Interests already exists!', 'danger')

        db.session.commit()
        return redirect(url_for('student_profile', studentID=current_user.id))

    #Deleting hobbies and Interests
    if choose_form.validate_on_submit():

        if choose_form.hobby_or_interest.data == 'hobby':
            q = db.select(Hobbies).where(Hobbies.id == int(choose_form.choice.data))
            hobby = db.session.scalar(q)

            if hobby:
                db.session.delete(hobby)
                db.session.commit()
                flash('Hobby deleted successfully!', 'info')
                return redirect(url_for('student_profile', studentID=current_user.id))

        elif choose_form.hobby_or_interest.data == 'interest':
            q = db.select(Interests).where(Interests.id == int(choose_form.choice.data))
            interest = db.session.scalar(q)

            if interest:
                db.session.delete(interest)
                db.session.commit()
                flash('Interest deleted successfully!', 'info')
                return redirect(url_for('student_profile', studentID=current_user.id))


    return render_template('student_profile.html', title='Student Profile', form=form, student=student,
                           choose_form=choose_form, edit_form=edit_form, student_id=str(studentID), hobbies_list=hobbies_list,
                           interests_list=interests_list)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    edit_form = EditPersonalDetailsForm()

    q = db.select(User).where(User.id == current_user.id)
    user = db.session.scalar(q)

    if edit_form.edit.data != '-1':
        # Populate db data to form
        edit_form.first_name.data = user.first_name
        edit_form.last_name.data = user.last_name
        edit_form.email.data = user.email
        edit_form.phone.data = user.phone
        edit_form.age.data = user.age
        edit_form.emergency_name.data = user.emergency_name
        edit_form.emergency_phone.data = user.emergency_phone

    return render_template('edit_personal_details.html', title='Edit Personal Details', edit_form=edit_form)


@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    edit_form = EditPersonalDetailsForm()
    if edit_form.validate_on_submit():
        q = db.select(User).where(User.id == current_user.id)
        user = db.session.scalar(q)

        # From form to db
        user.first_name = edit_form.first_name.data
        user.last_name = edit_form.last_name.data
        user.email = edit_form.email.data
        user.phone = edit_form.phone.data
        user.age = edit_form.age.data
        user.emergency_name = edit_form.emergency_name.data
        user.emergency_phone = edit_form.emergency_phone.data

        db.session.commit()
        flash('Your details have been updated successfully!', 'info')

    return redirect(url_for('student_profile', studentID=current_user.id))


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

@app.route('/book_meeting', methods=['GET', 'POST'])
@login_required
def book_meeting():
    form=MeetingForm()
    if form.validate_on_submit():
        meeting = Meeting(
            name=current_user.first_name,
            email=current_user.email,
            date=str(form.date.data),
            time=str(form.time.data)
        )
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting booked!', 'success')
        return redirect(url_for('home'))
    return render_template('book_meeting.html', title='Meeting', form=form)

# event calender feature

# Show events list
@app.route("/events")
def events():
    events_list = Event.query.order_by(Event.start_time).all()
    return render_template('events.html', events=events_list, now=datetime.now(), title="Event Calendar")

# Add new event
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            location=form.location.data,
            mode=form.mode.data,
            link=form.link.data if form.mode.data == "Online" else None,
            category=form.category.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('events'))

    return render_template('add_event.html', form=form, title="Add New Event")

# Delete an event
@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events'))







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