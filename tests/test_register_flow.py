import os
import tempfile
import pytest

from app import app, db
from models import User


@pytest.fixture(autouse=True)
def _configure_app(tmp_path, monkeypatch):
    """Set up a temporary SQLite DB for each test run and create tables."""
    # Use a temporary sqlite file so SQLAlchemy works reliably across threads
    db_file = tmp_path / "test_db.sqlite"
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'

    # Ensure we run initialization against the tmp DB
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
    yield
    # cleanup
    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_register_success():
    client = app.test_client()
    data = {
        'username': 'testuser1',
        'email': 'testuser1@example.com',
        'password': 'secret123',
        'area': 'Programación',
        'user_type': 'student'
    }
    resp = client.post('/register', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Registro exitoso. Ahora puedes iniciar sesi' in resp.data


def test_register_existing_username():
    with app.app_context():
        u = User(username='dupuser', email='dup@example.com', password='x', area='Programación')
        db.session.add(u)
        db.session.commit()

    client = app.test_client()
    data = {
        'username': 'dupuser',
        'email': 'newemail@example.com',
        'password': 'pw',
        'area': 'Programación',
        'user_type': 'student'
    }
    resp = client.post('/register', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b'El nombre de usuario ya est' in resp.data


def test_register_existing_email():
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
    resp = client.post('/register', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b'El correo electr' in resp.data


def test_register_missing_fields():
    client = app.test_client()
    data = {
        'username': '',
        'email': '',
        'password': '',
        'area': '',
        'user_type': ''
    }
    resp = client.post('/register', data=data, follow_redirects=True)
    assert resp.status_code == 200
    assert b'Todos los campos son obligatorios' in resp.data
