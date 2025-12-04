from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(200), nullable=False)
    area = db.Column(db.String(50)) 
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(300), default='https://api.dicebear.com/7.x/identicon/svg?seed=default')
    theme = db.Column(db.String(30), default='default')

    quizzes_created = db.relationship('Quiz', backref='creator', lazy=True)
    answers = db.relationship('UserAnswer', backref='user', lazy=True)
    achievements = db.relationship('Achievement', backref='user', lazy=True)
    messages = db.relationship('ChatMessage', backref='user', lazy=True)



class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    area = db.Column(db.String(50))  # Opcional: área principal del profesor
    cedula_profesional_img = db.Column(db.String(300), nullable=True)  # Ruta de la imagen de la cédula
    cedula_verified = db.Column(db.Boolean, default=False)  # Estado de verificación
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))
    quizzes = db.relationship('Quiz', backref='teacher', lazy=True)
    games = db.relationship('Game', backref='teacher', lazy=True)


class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    area = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('Question', backref='quiz', lazy=True)


class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    options = db.Column(db.JSON, nullable=False)  # Ej: ["A", "B", "C", "D"]
    correct_answer = db.Column(db.Text, nullable=False)

    answers = db.relationship('UserAnswer', backref='question', lazy=True)
    messages = db.relationship('ChatMessage', backref='question', lazy=True)


class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)



# Modelo para logros/insignias globales
class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(300))
    image_url = db.Column(db.String(300))  # URL o ruta de la imagen
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Logros obtenidos por usuario (relación con Badge)
class Achievement(db.Model):
    __tablename__ = 'achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relación para acceder a los datos del badge desde el achievement
    badge = db.relationship('Badge', backref='achievements', lazy=True)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))  # Ejemplo: quiz, memoria, puzzle, etc.
    rules = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # null = todos
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notifications', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    ip = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, nullable=False)