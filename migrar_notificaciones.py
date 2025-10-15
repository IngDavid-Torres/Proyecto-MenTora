from models import db, Notification

def run():
    db.create_all()
    print("Tablas creadas o actualizadas.")
