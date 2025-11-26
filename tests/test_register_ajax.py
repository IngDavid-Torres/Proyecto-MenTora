import pytest

from app import app, db
from models import User


@pytest.fixture(autouse=True)
def _configure_app(tmp_path, monkeypatch):
    db_file = tmp_path / "test_db.sqlite"
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_register_json_success():
    client = app.test_client()
    data = {
        'username': 'ajaxuser1',
        'email': 'ajax1@example.com',
        'password': 'secret123',
        'area': 'Programación',
        'user_type': 'student'
    }

    resp = client.post('/register', data=data, headers={'Accept': 'application/json'})
    assert resp.status_code == 200
    j = resp.get_json()
    assert isinstance(j, dict)
    assert j['success'] is True
    assert 'Registro exitoso' in j['message']


def test_register_json_existing_username():
    with app.app_context():
        u = User(username='dupusername', email='dup1@example.com', password='x', area='Programación')
        db.session.add(u)
        db.session.commit()

    client = app.test_client()
    data = {
        'username': 'dupusername',
        'email': 'newemail@example.com',
        'password': 'pw',
        'area': 'Programación',
        'user_type': 'student'
    }
    resp = client.post('/register', data=data, headers={'Accept': 'application/json'})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j['success'] is False
    assert 'nombre de usuario' in j['message']


def test_register_json_existing_email():
    with app.app_context():
        u = User(username='u2', email='exists@example.com', password='x', area='Programación')
        db.session.add(u)
        db.session.commit()

    client = app.test_client()
    data = {
        'username': 'anothername',
        'email': 'exists@example.com',
        'password': 'pw',
        'area': 'Programación',
        'user_type': 'student'
    }
    resp = client.post('/register', data=data, headers={'Accept': 'application/json'})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j['success'] is False
    assert 'correo' in j['message']


def test_register_json_missing_fields():
    client = app.test_client()
    data = {
        'username': '',
        'email': '',
        'password': '',
        'area': '',
        'user_type': ''
    }
    resp = client.post('/register', data=data, headers={'Accept': 'application/json'})
    assert resp.status_code == 400
    j = resp.get_json()
    assert j['success'] is False
    assert 'Todos los campos' in j['message']
