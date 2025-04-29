from flask import render_template, redirect, url_for, flash, request
from app import app, db
from app.models import Event
from app.forms import EventForm
from datetime import datetime

# Redirect to events page
@app.route("/")
def home():
    return redirect(url_for('events'))

# Show events list
@app.route("/events")
def events():
    events_list = Event.query.order_by(Event.start_time).all()
    return render_template('events.html', events=events_list, now=datetime.now())

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
            location=form.location.data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('events'))

    if request.method == 'POST':
        flash('Failed to add event. Please enter valid data.', 'danger')
        print("Form Errors:", form.errors)

    return render_template('add_event.html', form=form)

# Delete an event
@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('events'))
