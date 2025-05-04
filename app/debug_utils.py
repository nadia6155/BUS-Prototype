from app import db
from app.models import User
import datetime
from app.models import User,Meeting



def reset_db():
    db.drop_all()
    db.create_all()

    users =[
        {'first_name': 'amy', 'last_name': 'smith', 'email': 'amy@admin.com', 'role': 'Admin', 'pw': 'Mypassword123'},
        {'first_name': 'tom', 'last_name': 'smith', 'email': 'tom@student.com', 'role': 'Student', 'pw': 'Mypassword123'},
        {'first_name': 'yin', 'last_name': 'smith', 'email': 'yin@admin.com', 'role': 'Admin', 'pw': 'Mypassword123'},
        {'first_name': 'tariq', 'last_name': 'smith', 'email': 'trq@staff.com', 'role': 'Staff', 'pw': 'Mypassword123'},
        {'first_name': 'jo', 'last_name': 'smith', 'email': 'jo@student.com', 'role': 'Student', 'pw': 'Mypassword123'}
    ]

    for u in users:
        # get the password value and remove it from the dict:
        pw = u.pop('pw')
        # create a new user object using the parameters defined by the remaining entries in the dict:
        user = User(**u)
        # set the password for the user object:
        user.set_password(pw)
        # add the newly created user object to the database session:
        db.session.add(user)
    db.session.commit()
