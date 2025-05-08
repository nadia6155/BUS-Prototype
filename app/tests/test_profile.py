import pytest
from app.models import User

# positive test case
def pos_test_edit_profile(client):
    response = client.post('/edit_personal_details', data={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@staff.com',
        'edit': '-1'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Your details have been updated successfully!' in response.data

    # check edited profile added to db
    edited_profile = User.query.filter_by(email='john@staff.com').first()
    assert edited_profile.first_name == 'John'
    assert edited_profile.last_name == 'Doe'
    assert edited_profile is not None

# negative test case with missing first_name
def neg_test_edit_profile(client):
    response = client.post('/edit_personal_details', data={
        'first_name': '',
        'last_name': 'Doe',
        'email': 'john@staff.com',
        'edit': '-1'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Data required' in response.data

    # check edited profile has NOT been added to db
    profile = User.query.filter_by(email='john@staff.com').first()
    assert profile.first_name == ''
    assert profile is None