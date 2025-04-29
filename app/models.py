from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
import datetime
from datetime import datetime

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

    hobbies: so.Mapped[list['Hobbies']] = relationship(back_populates='user', cascade='all, delete-orphan')
    interests: so.Mapped[list['Interests']] = relationship(back_populates='user', cascade='all, delete-orphan')


    def __repr__(self):
        pwh= 'None' if not self.password_hash else f'...{self.password_hash[-5:]}'
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


# meetings booked table
class Meeting(db.Model):
    meeting_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))

# event calender table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
