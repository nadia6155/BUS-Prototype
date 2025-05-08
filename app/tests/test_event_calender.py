import pytest

# positive test case to add an event
def test_add_event(client):
    response = client.post('/add_event', data={
        'title': 'Test Event',
        'description': 'This is a test event.',
        'start_time': '2025-05-15T10:00',
        'end_time': '2025-05-15T11:00',
        'mode': 'In-person',
        'link': '',  # not needed for in-person
        'location': 'Test Room 101',
        'category': 'Academics',
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Event added successfully!' in response.data


# negative test case to add online event without link
def test_add_online_event_without_link(client):
    response = client.post('/add_event', data={
        'title': 'Event for test',
        'description': 'No link given',
        'start_time': '2025-05-15T10:00',
        'end_time': '2025-05-15T11:00',
        'mode': 'Online',
        'link': '',  # missing link
        'location': '',
        'category': 'well-being'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'This field is required for online events' in response.data
