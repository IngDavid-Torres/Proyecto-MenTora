from app import app, db
from models import User


def setup_tmp_db():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.drop_all()
        db.create_all()


def run_all():
    setup_tmp_db()
    client = app.test_client()

    tests = []

    # 1 success
    data = {'username': 'smoke1', 'email': 'smoke1@example.com', 'password': 'pw', 'area': 'Programación', 'user_type': 'student'}
    resp = client.post('/register', data=data, follow_redirects=True)
    tests.append(('register_success', resp.status_code == 200 and b'Registro exitoso' in resp.data))

    # reset db
    with app.app_context():
        db.drop_all(); db.create_all()

    # 2 existing username
    with app.app_context():
        u = User(username='dupuser', email='dup@example.com', password='x', area='Programación')
        db.session.add(u); db.session.commit()
    data = {'username': 'dupuser', 'email': 'new@example.com', 'password': 'pw', 'area': 'Programación', 'user_type': 'student'}
    resp = client.post('/register', data=data, follow_redirects=True)
    tests.append(('existing_username', resp.status_code == 200 and b'El nombre de usuario' in resp.data))

    # 3 existing email
    with app.app_context():
        db.drop_all(); db.create_all()
        u = User(username='u2', email='exists@example.com', password='x', area='Programación')
        db.session.add(u); db.session.commit()
    data = {'username': 'another', 'email': 'exists@example.com', 'password': 'pw', 'area': 'Programación', 'user_type': 'student'}
    resp = client.post('/register', data=data, follow_redirects=True)
    tests.append(('existing_email', resp.status_code == 200 and b'El correo' in resp.data))

    # 4 missing fields
    with app.app_context():
        db.drop_all(); db.create_all()
    data = {'username':'', 'email':'', 'password':'', 'area':'', 'user_type':''}
    resp = client.post('/register', data=data, follow_redirects=True)
    tests.append(('missing_fields', resp.status_code == 200 and b'Todos los campos son obligatorios' in resp.data))

    ok = True
    for name, passed in tests:
        print(f"{name}: {'OK' if passed else 'FAIL'}")
        if not passed: ok = False
    print('\nALL OK' if ok else '\nSOME FAIL')


if __name__ == '__main__':
    run_all()
