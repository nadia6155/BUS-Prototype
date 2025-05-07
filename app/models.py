from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime


@dataclass
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    role: so.Mapped[str] = so.mapped_column(sa.String(10), default="Normal")
    phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), unique=True)
    age: so.Mapped[Optional[int]] = so.mapped_column()
    emergency_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    emergency_phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(120), unique=True)

    # Rewards
    points: so.Mapped[int] = so.mapped_column(default=0)
    last_login_date: so.Mapped[datetime.datetime] = so.mapped_column(default=None, nullable=True)

    hobbies: so.Mapped[list['Hobbies']] = relationship(back_populates='user', cascade='all, delete-orphan')
    interests: so.Mapped[list['Interests']] = relationship(back_populates='user', cascade='all, delete-orphan')

    #Meeting-user relationship
    user_meeting: so.Mapped[list['Meeting']] = relationship(back_populates='user', foreign_keys='Meeting.user_id', cascade="all, delete-orphan")
    staff_meeting: so.Mapped[list['Meeting']] = relationship(back_populates='staff', foreign_keys='Meeting.staff_id', cascade="all, delete-orphan")

    # notification-user composition relationship
    notifications: so.Mapped[list['Notification']] = relationship(back_populates='user',
                                                                  cascade="all,delete-orphan",
                                                                  passive_deletes=True,
                                                                  single_parent=True)
    def __repr__(self):
        pwh = 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
        return f'User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email}, role={self.role}, phone={self.phone}, pwh={pwh})'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Hobbies(db.Model):
    __tablename__ = 'hobbies'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    hobbies: so.Mapped[str] = so.mapped_column(sa.String(120))
    user_id: so.Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user: so.Mapped['User'] = relationship(back_populates='hobbies')

class Interests(db.Model):
    __tablename__ = 'interests'

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    interests: so.Mapped[str] = so.mapped_column(sa.String(120))
    user_id: so.Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    user: so.Mapped['User'] = relationship(back_populates='interests')


# meetings booked model
class Meeting(db.Model):
    __tablename__ = 'meetings'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100))
    email: so.Mapped[str] = so.mapped_column(sa.String(100))
    date: so.Mapped[datetime.date] = so.mapped_column(sa.Date)
    time_slot: so.Mapped[str] = so.mapped_column(sa.String(20))

    # meeting-user relationship
    user_id: so.Mapped[int] = so.mapped_column(ForeignKey('users.id'), index=True)
    staff_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'), index=True)

    user: so.Mapped['User'] = relationship(back_populates='user_meeting', foreign_keys=[user_id])
    staff: so.Mapped['User'] = relationship(back_populates='staff_meeting', foreign_keys=[staff_id])

    def __repr__(self):
        return f'Meeting(id={self.id}, date={self.date}, time_slot={self.time_slot},user_id={self.user_id})'

# notification model
class Notification(db.Model):
    __tablename__ = 'notification'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(sa.String(100))

    # notification-user composition relationship
    user_id: so.Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), index=True)
    user: so.Mapped['User'] = relationship(back_populates='notifications')

# event calender table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    mode = db.Column(db.String(10), nullable=False)  # 'Online' or 'In-person'
    link = db.Column(db.String(255), nullable=True)  # For online events
    category = db.Column(db.String(50), nullable=False)  # 'University', 'Society', 'Uni Support'
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
