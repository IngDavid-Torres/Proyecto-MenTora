from app import db
from models import Badge

def run():
    db.create_all()
    print('Tablas creadas o actualizadas (incluyendo Badge).')

if __name__ == '__main__':
    run()
