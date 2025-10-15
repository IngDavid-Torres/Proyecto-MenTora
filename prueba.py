from app import db, User # type: ignore
admin = User.query.filter_by(username='admin').first()
print(admin.password)