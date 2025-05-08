import pytest
from app.models import Meeting, User

# positive test case
def pos_test_meeting(client):
    response = client.post('/book_meeting', data={
        'date': '2025-05-10',
        'time_slot': '09:00 AM',
        'staff': User.id
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Meeting booked successfully!' in response.data

    # check meeting added to db
    booked_meeting = Meeting.query.filter_by(date='2025-05-10').first()
    assert booked_meeting.time_slot == '09:00 AM'
    assert booked_meeting is not None

# negative test case with missing date
def neg_test_meeting(client):
    response = client.post('/book_meeting', data={
        'date': '',
        'time_slot': '09:00 AM',
        'staff': User.id
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'invalid-feedback' in response.data

    # check meeting has NOT been added to db
    meeting = Meeting.query.filter_by(time_slot='09:00 AM').first()
    assert meeting is None