import os
import time
from datetime import datetime


from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import Markup


from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models import db, User, Quiz, Question, UserAnswer, Achievement, Badge, Notification, AccessLog, Teacher


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)
socketio = SocketIO(app)

@app.route('/chat')
def chat():
    return render_template('chat.html')



chat_history = []


@socketio.on('send_message')
def handle_send_message(data):
    import re
    username = data.get('username', 'Invitado')
    message = data.get('message', '')
    # Reemplazar atajos de emoji por emojis reales
    emoji_map = {
        ':)': '😊', ':(': '😢', ':D': '😃', '<3': '❤️', ':o': '😮', ':p': '😛', ':fire:': '🔥', ':star:': '⭐', ':ok:': '👌', ':cool:': '😎', ':rocket:': '🚀', ':100:': '💯', ':party:': '🥳', ':clap:': '👏', ':sad:': '😔', ':up:': '👍', ':down:': '👎', ':wink:': '😉', ':joy:': '😂', ':cry:': '😭', ':angry:': '😠', ':heart:': '❤️', ':check:': '✅', ':x:': '❌', ':star2:': '🌟', ':tada:': '🎉', ':wave:': '👋', ':smile:': '😄', ':sunglasses:': '😎', ':thinking:': '🤔', ':sleep:': '😴', ':zzz:': '💤', ':hug:': '🤗', ':pray:': '🙏', ':muscle:': '💪', ':eyes:': '👀', ':see_no_evil:': '🙈', ':poop:': '💩', ':cat:': '🐱', ':dog:': '🐶', ':robot:': '🤖', ':star-struck:': '🤩', ':mindblown:': '🤯', ':nerd:': '🤓', ':money:': '🤑', ':sweat:': '😅', ':kiss:': '😘', ':hugging:': '🤗', ':confetti:': '🎊', ':medal:': '🏅', ':trophy:': '🏆', ':crown:': '👑', ':medal2:': '🎖️', ':medal3:': '🥇', ':medal4:': '🥈', ':medal5:': '🥉', ':star3:': '⭐️', ':star4:': '🌠', ':star5:': '✨', ':star6:': '🌟', ':star7:': '💫', ':star8:': '🌟', ':star9:': '🌟', ':star10:': '🌟', ':star11:': '🌟', ':star12:': '🌟', ':star13:': '🌟', ':star14:': '🌟', ':star15:': '🌟', ':star16:': '🌟', ':star17:': '🌟', ':star18:': '🌟', ':star19:': '🌟', ':star20:': '🌟', ':star21:': '🌟', ':star22:': '🌟', ':star23:': '🌟', ':star24:': '🌟', ':star25:': '🌟', ':star26:': '🌟', ':star27:': '🌟', ':star28:': '🌟', ':star29:': '🌟', ':star30:': '🌟', ':star31:': '🌟', ':star32:': '🌟', ':star33:': '🌟', ':star34:': '🌟', ':star35:': '🌟', ':star36:': '🌟', ':star37:': '🌟', ':star38:': '🌟', ':star39:': '🌟', ':star40:': '🌟', ':star41:': '🌟', ':star42:': '🌟', ':star43:': '🌟', ':star44:': '🌟', ':star45:': '🌟', ':star46:': '🌟', ':star47:': '🌟', ':star48:': '🌟', ':star49:': '🌟', ':star50:': '🌟'
    }
    def replace_emojis(text):
        for k, v in emoji_map.items():
            text = text.replace(k, v)
        return text
    message = replace_emojis(message)
    chat_history.append({'username': username, 'message': message})
    if len(chat_history) > 50:
        chat_history.pop(0)
    emit('receive_message', {'username': username, 'message': message}, broadcast=True)

# Evento para enviar historial al conectarse
@socketio.on('request_history')
def handle_request_history():
    emit('chat_history', chat_history)


with app.app_context():
    db.create_all()
    print("✅ Tablas creadas correctamente.")

    admin = User.query.filter_by(username='admin').first()
    if admin:
        admin.password = generate_password_hash('admin123')
        admin.email = 'admin@mentora.com'
        admin.area = 'general'
        admin.is_admin = True
        db.session.commit()
        print("🔐 Usuario admin actualizado.")
    else:
        admin_user = User(
            username='admin',
            email='admin@mentora.com',
            password=generate_password_hash('admin123'),
            area='general',
            is_admin=True,
            points=0,
            level=1
        )
        db.session.add(admin_user)
        db.session.commit()
        print("👑 Usuario administrador creado.")

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        area = request.form['area']
        user_type = request.form.get('user_type', 'student')

        if not username or not email or not password or not area or not user_type:
            msg = 'Todos los campos son obligatorios.'
            if request.accept_mimetypes['application/json']:
                return jsonify(success=False, message=msg), 400
            flash(msg)
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()
        if existing_user:
            msg = 'El nombre de usuario ya está en uso.'
            if request.accept_mimetypes['application/json']:
                return jsonify(success=False, message=msg), 400
            flash(msg)
            return redirect(url_for('register'))
        if existing_email:
            msg = 'El correo electrónico ya está registrado.'
            if request.accept_mimetypes['application/json']:
                return jsonify(success=False, message=msg), 400
            flash(msg)
            return redirect(url_for('register'))

        try:
            hashed_password = generate_password_hash(password)
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                area=area,
                points=0,
                level=1,
                is_admin=False
            )
            db.session.add(new_user)
            db.session.flush()  # Para obtener el id
            if user_type == 'teacher':
                teacher = Teacher(user_id=new_user.id, area=area)
                db.session.add(teacher)
            db.session.commit()
            msg = 'Registro exitoso. Ahora puedes iniciar sesión.'
            if request.accept_mimetypes['application/json']:
                return jsonify(success=True, message=msg)
            flash(msg)
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            msg = 'Error interno en el registro.'
            if request.accept_mimetypes['application/json']:
                return jsonify(success=False, message=msg), 500
            flash(msg)
            return redirect(url_for('register'))

    return render_template('register.html')

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        ip = request.remote_addr or 'unknown'
        success = user is not None and check_password_hash(user.password, password)
        # Registrar log de acceso
        log = AccessLog(username=username, ip=ip, success=success)
        db.session.add(log)
        db.session.commit()
        if success:
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            session['avatar_url'] = user.avatar_url if user.avatar_url else ''
            session['theme'] = user.theme if user.theme else 'default'
            # Redirección según tipo de usuario
            if user.is_admin:
                return jsonify(success=True, redirect=url_for('admin_panel'))
            elif hasattr(user, 'teacher_profile') and user.teacher_profile is not None:
                return jsonify(success=True, redirect=url_for('teacher_dashboard'))
            else:
                return jsonify(success=True, redirect=url_for('dashboard'))
        else:
            return jsonify(success=False), 401

    # Solo GET: renderizar formulario
    return render_template('login.html')

# Panel del usuario
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Reto diario/semanal: selecciona un quiz aleatorio del área del usuario, cambia cada día
    from datetime import date
    import random
    daily_seed = int(date.today().strftime('%Y%m%d'))
    quizzes_in_area = Quiz.query.filter_by(area=user.area).all()
    daily_quiz = None
    if quizzes_in_area:
        random.seed(daily_seed)
        daily_quiz = random.choice(quizzes_in_area)
    from sqlalchemy.orm import joinedload
    achievements = Achievement.query.options(joinedload(Achievement.badge)).filter_by(user_id=user.id).all()
    # Mostrar quizzes creados por el profesor actual o el admin, con preguntas asociadas
    admin_user = User.query.filter_by(is_admin=True).first()
    # Obtener perfil de profesor si existe
    # Refuerza la obtención del perfil de profesor
    from models import Teacher
    teacher = None
    if hasattr(user, 'teacher_profile') and user.teacher_profile is not None:
        teacher = user.teacher_profile
    else:
        teacher = Teacher.query.filter_by(user_id=user.id).first()

    from sqlalchemy import or_
    quizzes_all = Quiz.query.filter(
            or_(Quiz.area == user.area, Quiz.teacher_id != None, Quiz.teacher_id == None)
    ).all()
    quizzes = []
    for q in quizzes_all:
        tiene_preguntas = hasattr(q, 'questions') and q.questions and len(q.questions) > 0
        es_del_profesor = teacher is not None and hasattr(q, 'teacher_id') and q.teacher_id == teacher.id
        es_del_admin = (
            (hasattr(q, 'teacher') and getattr(q.teacher, 'is_admin', False)) or
            (q.teacher_id is None)
        )
        if tiene_preguntas and (es_del_profesor or es_del_admin):
            quizzes.append(q)
    from models import Game
    games_all = Game.query.filter(
        or_(Game.area == user.area, Game.teacher_id == None)
    ).all() if hasattr(Game, 'area') else []
    games = []
    for g in games_all:
        es_del_profesor = teacher is not None and hasattr(g, 'teacher_id') and g.teacher_id == teacher.id
        es_del_admin = (
            (hasattr(g, 'teacher') and getattr(g.teacher, 'is_admin', False)) or
            (g.teacher_id is None)
        )
        if es_del_profesor or es_del_admin:
            games.append(g)
    # Historial de actividad: últimos 5 retos respondidos y logros obtenidos
    last_answers = (
        db.session.query(UserAnswer, Question, Quiz)
        .join(Question, UserAnswer.question_id == Question.id)
        .join(Quiz, Question.quiz_id == Quiz.id)
        .filter(UserAnswer.user_id == user.id)
        .order_by(UserAnswer.answered_at.desc())
        .limit(5)
        .all()
    )
    last_achievements = Achievement.query.filter_by(user_id=user.id).order_by(Achievement.earned_at.desc()).limit(5).all()

    
    points_this_level = user.points - ((user.level - 1) * 100)
    points_needed = 100
    progress_percent = int((points_this_level / points_needed) * 100) if user.level > 0 else 0
    if progress_percent > 100:
        progress_percent = 100
        # Calcular progreso considerando quizzes de profesor con 15 puntos y admin con 10
        points_this_level = 0
        quizzes_answered_ids = db.session.query(Question.quiz_id).join(UserAnswer).filter(UserAnswer.user_id == user.id).distinct().all()
        quizzes_answered = set(qid for (qid,) in quizzes_answered_ids)
        for q in quizzes:
            if q.id in quizzes_answered:
                if q.teacher_id:
                    points_this_level += 15
                else:
                    points_this_level += 10
        points_this_level += user.points - ((user.level - 1) * 100)

   
    if progress_percent == 100:
        motivational_message = "¡Felicidades! Has alcanzado un nuevo nivel. ¡Sigue así!"
    elif progress_percent >= 75:
        motivational_message = "¡Estás muy cerca de subir de nivel!"
    elif progress_percent >= 50:
        motivational_message = "¡Vas por la mitad, no te detengas!"
    elif progress_percent >= 25:
        motivational_message = "¡Buen progreso! Sigue participando para subir de nivel."
    else:
        motivational_message = "¡Cada reto cuenta! Responde más para avanzar."

    # Ranking: top 10 usuarios por puntos
    leaderboard = User.query.filter_by(is_admin=False).order_by(User.points.desc(), User.level.desc()).limit(10).all()


    # Progreso de retos completados
    total_quizzes = Quiz.query.filter_by(area=user.area).count()
    quizzes_answered_ids = db.session.query(Question.quiz_id).join(UserAnswer).filter(UserAnswer.user_id == user.id).distinct().all()
    quizzes_answered = len(set(qid for (qid,) in quizzes_answered_ids))
    if total_quizzes > 0:
        quiz_progress_percent = int((quizzes_answered / total_quizzes) * 100)
    else:
        quiz_progress_percent = 0

    # Notificaciones: mostrar solo las globales y las dirigidas a este usuario
    notifications = Notification.query.filter(
        (Notification.to_user == None) | (Notification.to_user == user.id)
    ).order_by(Notification.date_sent.desc()).limit(5).all()

    return render_template('dashboard.html',
                           username=user.username,
                           area=user.area,
                           points=user.points,
                           level=user.level,
                           achievements=achievements,
                           quizzes=quizzes,
                           games=games,
                           progress_percent=progress_percent,
                           motivational_message=motivational_message,
                           leaderboard=leaderboard,
                           total_quizzes=total_quizzes,
                           quizzes_answered=quizzes_answered,
                           quiz_progress_percent=quiz_progress_percent,
                           last_answers=last_answers,
                           last_achievements=last_achievements,
                           notifications=notifications,
                           avatar_url=user.avatar_url,
                           theme=session.get('theme', user.theme if user.theme else 'default'),
                           daily_quiz=daily_quiz,
                           teacher=teacher)

# Reto activo
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    # Si es GET y no se está intentando un quiz específico, mostrar lista de quizzes disponibles
    from sqlalchemy import or_
    quizzes_all = Quiz.query.filter(
        or_(Quiz.area == user.area, Quiz.teacher_id == None)
    ).all()
    quizzes = []
    for q in quizzes_all:
        tiene_preguntas = hasattr(q, 'questions') and q.questions and len(q.questions) > 0
        if tiene_preguntas:
            quizzes.append(q)
    # Si no es POST, mostrar lista de quizzes
    if request.method == 'GET' and not request.args.get('quiz_id'):
        return render_template('quiz.html', all_quizzes=quizzes)

    # Si es POST o se está intentando un quiz aleatorio (legacy)
    question = Question.query.join(Quiz).filter(Quiz.area == user.area).order_by(db.func.random()).first()
    if not question:
        flash('No hay preguntas disponibles en tu área aún.')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        selected = request.form.get('selected_answer')
        is_correct = selected == question.correct_answer
        answer = UserAnswer(
            user_id=user.id,
            question_id=question.id,
            selected_answer=selected,
            is_correct=is_correct,
            answered_at=datetime.utcnow()
        )
        db.session.add(answer)
        if is_correct:
            user.points += 10
            if user.points >= user.level * 100:
                user.level += 1

            # Otorgar logro por primer quiz correcto
            from models import Achievement, Badge
            primer_quiz_badge = Badge.query.filter_by(name='Primer Quiz').first()
            if primer_quiz_badge:
                ya_tiene = Achievement.query.filter_by(user_id=user.id, badge_id=primer_quiz_badge.id).first()
                if not ya_tiene:
                    nuevo_logro = Achievement(user_id=user.id, badge_id=primer_quiz_badge.id)
                    db.session.add(nuevo_logro)
        db.session.commit()

        flash('Respuesta registrada. ' + ('¡Correcto!' if is_correct else 'Incorrecto.'))
        return redirect(url_for('dashboard'))

    return render_template('quiz.html', question=question)


@app.route('/admin', methods=['GET'])
def admin_panel():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido. Solo administradores.')
        return redirect(url_for('login'))

    total_users = User.query.count()
    total_quizzes = Quiz.query.count()
    total_questions = Question.query.count()
    users = User.query.filter(User.username != 'admin').all()
    user_to_edit = session.pop('user_to_edit', None)
    from models import Game
    games = Game.query.order_by(Game.created_at.desc()).all()
    game_to_edit = session.get('game_to_edit', None)
    quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    achievements = Badge.query.order_by(Badge.created_at.desc()).all()
    achievement_to_edit = session.pop('achievement_to_edit', None)
    # Notificaciones: últimas 20
    notifications = Notification.query.order_by(Notification.date_sent.desc()).limit(20).all()
    # Logs de acceso: últimos 20
    access_logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(20).all()
    return render_template('admin.html',
                           username=session['username'],
                           total_users=total_users,
                           total_quizzes=total_quizzes,
                           total_questions=total_questions,
                           users=users,
                           user_to_edit=user_to_edit,
                           games=games,
                           game_to_edit=game_to_edit,
                           quizzes=quizzes,
                           achievements=achievements,
                           achievement_to_edit=achievement_to_edit,
                           notifications=notifications,
                           access_logs=access_logs)
# Cambiar contraseña de admin
@app.route('/admin/change_password', methods=['POST'])
def change_admin_password():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    admin = User.query.get(session['user_id'])
    if not check_password_hash(admin.password, current_password):
        flash('La contraseña actual es incorrecta.')
        return redirect(url_for('admin_panel'))
    if new_password != confirm_password:
        flash('La nueva contraseña y la confirmación no coinciden.')
        return redirect(url_for('admin_panel'))
    if len(new_password) < 6:
        flash('La nueva contraseña debe tener al menos 6 caracteres.')
        return redirect(url_for('admin_panel'))
    admin.password = generate_password_hash(new_password)
    db.session.commit()
    flash('Contraseña actualizada correctamente.')
    return redirect(url_for('admin_panel'))


@app.route('/admin/send_notification', methods=['POST'])
def send_notification():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    message = request.form.get('notification_message', '').strip()
    to_user = request.form.get('notification_user')
    if not message:
        flash('El mensaje no puede estar vacío.')
        return redirect(url_for('admin_panel'))
    if to_user == 'all':
        notif = Notification(message=message, to_user=None)
        db.session.add(notif)
    else:
        try:
            user_id = int(to_user)
            notif = Notification(message=message, to_user=user_id)
            db.session.add(notif)
        except Exception:
            flash('Usuario destino inválido.')
            return redirect(url_for('admin_panel'))
    db.session.commit()
    flash('Notificación enviada.')
    return redirect(url_for('admin_panel'))


@app.route('/admin/create_or_update_achievement', methods=['POST'])
def create_or_update_achievement():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    achievement_id = request.form.get('achievement_id')
    name = request.form['achievement_name'].strip()
    description = request.form['achievement_description'].strip()
    image_file = request.files.get('achievement_image')
    image_url = None
    if image_file and image_file.filename:
        filename = secure_filename(image_file.filename)
        img_folder = os.path.join('static', 'img', 'badges')
        os.makedirs(img_folder, exist_ok=True)
        img_path = os.path.join(img_folder, filename)
        image_file.save(img_path)
        image_url = f'/static/img/badges/{filename}'
    if achievement_id:
        badge = Badge.query.get(achievement_id)
        if badge:
            badge.name = name
            badge.description = description
            if image_url:
                badge.image_url = image_url
            db.session.commit()
            flash('Logro/insignia actualizado.')
    else:
        badge = Badge(name=name, description=description, image_url=image_url)
        db.session.add(badge)
        db.session.commit()
        flash('Logro/insignia creado.')
    return redirect(url_for('admin_panel'))


@app.route('/admin/edit_achievement/<int:badge_id>', methods=['GET'])
def edit_achievement(badge_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    badge = Badge.query.get_or_404(badge_id)
    session['achievement_to_edit'] = {
        'id': badge.id,
        'name': badge.name,
        'description': badge.description,
        'image_url': badge.image_url
    }
    return redirect(url_for('admin_panel'))


@app.route('/admin/clear_achievement_edit')
def clear_achievement_edit():
    session.pop('achievement_to_edit', None)
    return redirect(url_for('admin_panel'))


@app.route('/admin/delete_achievement/<int:badge_id>', methods=['POST'])
def delete_achievement(badge_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    badge = Badge.query.get_or_404(badge_id)
    db.session.delete(badge)
    db.session.commit()
    flash('Logro/insignia eliminado.')
    return redirect(url_for('admin_panel'))
# Ruta para crear juego desde admin
@app.route('/admin/create_game', methods=['POST'])

def create_game():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))

    from models import Game
    game_id = request.form.get('game_id')
    name = request.form.get('game_name', '').strip()
    description = request.form.get('game_description', '').strip()
    rules = request.form.get('game_rules', '').strip()

    if not name or not description:
        flash('Todos los campos obligatorios deben estar llenos.')
        return redirect(url_for('admin_panel'))

    try:
        if game_id:  # Editar juego existente
            game = Game.query.get_or_404(game_id)
            game.name = name
            game.description = description
            game.rules = rules
            db.session.commit()
            flash(f'Juego "{name}" actualizado correctamente.')
        else:  # Crear nuevo juego
            new_game = Game(name=name, description=description, rules=rules, teacher_id=None, created_at=datetime.utcnow())
            db.session.add(new_game)
            db.session.commit()
            flash(f'Juego "{name}" creado exitosamente.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al procesar el juego: {e}')
    
    # Limpiar datos de edición
    session.pop('game_to_edit', None)
    return redirect(url_for('admin_panel'))

# Eliminar juego
@app.route('/admin/delete_game/<int:game_id>', methods=['POST'])
def delete_game(game_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    
    from models import Game
    game = Game.query.get_or_404(game_id)
    
    try:
        db.session.delete(game)
        db.session.commit()
        flash(f'Juego "{game.name}" eliminado correctamente.')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el juego: {e}')
    
    return redirect(url_for('admin_panel'))

# Editar juego (cargar en formulario)
@app.route('/admin/edit_game/<int:game_id>', methods=['GET'])
def edit_game(game_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    
    from models import Game
    game = Game.query.get_or_404(game_id)
    session['game_to_edit'] = {
        'id': game.id,
        'name': game.name,
        'description': game.description,
        'rules': game.rules
    }
    return redirect(url_for('admin_panel'))

# Cancelar edición de juego
@app.route('/admin/clear_game_edit')
def clear_game_edit():
    session.pop('game_to_edit', None)
    return redirect(url_for('admin_panel'))

# Ruta para crear quiz desde admin
@app.route('/admin/create_quiz', methods=['POST'])

def create_quiz():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))

    title = request.form.get('quiz_name', '').strip()
    area = request.form.get('quiz_area', '').strip()
    description = request.form.get('quiz_description', '').strip()

    if not title or not area or not description:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('admin_panel'))

    # Si el usuario es admin, teacher_id debe ser None
    new_quiz = Quiz(
        title=title,
        area=area,
        description=description,
        created_by=session['user_id'],
        teacher_id=None,
        created_at=datetime.utcnow()
    )
    db.session.add(new_quiz)
    db.session.commit()
    flash(f'Quiz "{title}" creado exitosamente.')
    return redirect(url_for('admin_panel'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.')
    response = redirect(url_for('login'))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    # Invalida cookies de sesión
    response.set_cookie('session', '', expires=0)
    return response

@app.route('/edit_profile', methods=['GET'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    # Opciones de temas y avatares
    themes = ['default', 'dark', 'light', 'blue', 'green', 'pink']
    avatar_seeds = ['default', 'cat', 'dog', 'robot', 'coder', 'star', 'rocket', 'owl', 'fox', 'lion', 'panda', 'alien', 'ninja', 'wizard', 'unicorn', 'dragon']
    return render_template('edit_profile.html', user=user, themes=themes, avatar_seeds=avatar_seeds)


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    new_email = request.form['email'].strip()
    new_area = request.form['area']
    new_avatar_seed = request.form.get('avatar_seed')
    new_theme = request.form.get('theme')

    if new_email:
        user.email = new_email
    if new_area:
        user.area = new_area
    if new_avatar_seed:
        user.avatar_url = f"https://api.dicebear.com/7.x/identicon/svg?seed={new_avatar_seed}"
    if new_theme:
        user.theme = new_theme

    db.session.commit()
    # Actualizar sesión
    session['avatar_url'] = user.avatar_url if user.avatar_url else ''
    session['theme'] = user.theme if user.theme else 'default'
    if request.headers.get('Accept') == 'application/json':
        return jsonify(success=True, theme=session['theme'])
    flash('Perfil actualizado correctamente.')
    return redirect(url_for('dashboard'))



@app.route('/games')
def games():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    from models import User, Quiz, Game
    from sqlalchemy import or_
    user = User.query.get(session['user_id'])
    # Quizzes igual que en dashboard
    quizzes_all = Quiz.query.filter(
        or_(Quiz.area == user.area, Quiz.teacher_id == None)
    ).all()
    quizzes = []
    for q in quizzes_all:
        tiene_preguntas = hasattr(q, 'questions') and q.questions and len(q.questions) > 0
        if tiene_preguntas:
            quizzes.append(q)
    # Juegos igual que en dashboard
    games_all = Game.query.filter(
        or_(Game.area == user.area, Game.teacher_id == None)
    ).all() if hasattr(Game, 'area') else Game.query.order_by(Game.name).all()
    games = []
    for g in games_all:
        games.append(g)
    return render_template('games.html', quizzes=quizzes, games=games)

@app.route('/juegos-interactivos')
def juegos_interactivos():
    """Ruta para los juegos interactivos (programación y VR)"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('juegos_interactivos.html', 
                         username=user.username,
                         user_id=user.id,
                         avatar_url=user.avatar_url,
                         theme=session.get('theme', user.theme if user.theme else 'default'))


@app.route('/games/<int:game_id>/run', methods=['POST'])
def run_game_code(game_id):
    from models import Game, User
    import io, contextlib, time
    game = Game.query.get_or_404(game_id)
    code = request.form.get('code', '')
    output = ''
    feedback = ''
    max_attempts = 3
    cooldown_minutes = 30
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    # Guardar intentos y cooldown en sesión por usuario y juego
    session_key = f'game_{game_id}_attempts'
    session_cooldown_key = f'game_{game_id}_cooldown'
    attempts = session.get(session_key, 0)
    cooldown_until = session.get(session_cooldown_key)
    import datetime
    now = int(time.time())
    # Si está en cooldown
    if cooldown_until and now < cooldown_until:
        mins_left = int((cooldown_until - now) / 60) + 1
        feedback = f'Sin vidas. Intenta de nuevo en {mins_left} minutos.'
        return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=max_attempts, max_attempts=max_attempts, cooldown=True)
    # Si no está en cooldown, resetear si ya pasó
    if cooldown_until and now >= cooldown_until:
        attempts = 0
        session[session_key] = 0
        session.pop(session_cooldown_key, None)
    # Solo permitir si tiene intentos
    if attempts >= max_attempts:
        session[session_cooldown_key] = now + cooldown_minutes * 60
        feedback = f'Sin vidas. Intenta de nuevo en {cooldown_minutes} minutos.'
        return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=max_attempts, max_attempts=max_attempts, cooldown=True)
    # Evaluar código
    if game.name.lower() == 'hola mundo':
        safe_builtins = {'print': print}
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, {'__builtins__': safe_builtins})
            output = buf.getvalue()
        except Exception as e:
            output = f'Error: {str(e)}'
        # Validar si acertó (print exacto)
        if output.strip() == 'Hola mundo':
            feedback = '¡Correcto! Ganaste +10 puntos.'
            
            progress_percent = session.get('progress_percent', None)
            if progress_percent is None:
                
                points_this_level = user.points - ((user.level - 1) * 100)
                points_needed = 100
                progress_percent = int((points_this_level / points_needed) * 100) if user.level > 0 else 0
            progress_percent += 10
            user.points += 10
            
            if progress_percent >= 100 or user.points >= user.level * 100:
                progress_percent = 0
                user.level += 1
                feedback = '¡Excelente, así se hace! ¡Subes de nivel!'
            session['progress_percent'] = progress_percent
            db.session.commit()
            # Resetear intentos tras éxito
            session[session_key] = 0
            session.pop(session_cooldown_key, None)
            return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=0, max_attempts=max_attempts, success=True, show_animated_alert=True)
        else:
            attempts += 1
            session[session_key] = attempts
            if attempts >= max_attempts:
                session[cooldown_key] = now + cooldown_minutes * 60
                feedback = f'Incorrecto. Sin vidas. Intenta de nuevo en {cooldown_minutes} minutos.'
                return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=attempts, max_attempts=max_attempts, cooldown=True)
            else:
                feedback = f'Incorrecto. Intentos restantes: {max_attempts - attempts}'
    elif game.name.lower() == 'la suma de dos números':
        safe_builtins = {'print': print}
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(code, {'__builtins__': safe_builtins})
            output = buf.getvalue()
        except Exception as e:
            output = f'Error: {str(e)}'
        import re
        nums = re.findall(r'(\d+)', code)
        if len(nums) >= 2:
            a, b = int(nums[0]), int(nums[1])
            suma_esperada = a + b
            try:
                salida = int(output.strip())
            except Exception:
                salida = None
            if salida == suma_esperada:
                feedback = '¡Correcto! Ganaste +10 puntos.'
                progress_percent = session.get('progress_percent', None)
                if progress_percent is None:
                    points_this_level = user.points - ((user.level - 1) * 100)
                    points_needed = 100
                    progress_percent = int((points_this_level / points_needed) * 100) if user.level > 0 else 0
                progress_percent += 10
                user.points += 10
                if progress_percent >= 100 or user.points >= user.level * 100:
                    progress_percent = 0
                    user.level += 1
                    feedback = '¡Excelente, así se hace! ¡Subes de nivel!'
                session['progress_percent'] = progress_percent
                db.session.commit()
                session[session_key] = 0
                session.pop(session_cooldown_key, None)
                return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=0, max_attempts=max_attempts, success=True, show_animated_alert=True)
            else:
                attempts += 1
                session[session_key] = attempts
                if attempts >= max_attempts:
                    session[cooldown_key] = now + cooldown_minutes * 60
                    feedback = f'Incorrecto. Sin vidas. Intenta de nuevo en {cooldown_minutes} minutos.'
                    return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=attempts, max_attempts=max_attempts, cooldown=True)
                else:
                    feedback = f'Incorrecto. Intentos restantes: {max_attempts - attempts}'
        else:
            feedback = 'Por favor, define dos números en tu código.'
    return render_template('game_detail.html', game=game, output=output, feedback=feedback, attempts=attempts, max_attempts=max_attempts)
@app.route('/games/<int:game_id>')
def game_detail(game_id):
    from models import Game
    game = Game.query.get_or_404(game_id)
    # Para mostrar vidas aunque sea GET
    max_attempts = 3
    session_key = f'game_{game_id}_attempts'
    session_cooldown_key = f'game_{game_id}_cooldown'
    attempts = session.get(session_key, 0)
    import time
    now = int(time.time())
    cooldown_until = session.get(session_cooldown_key)
    cooldown = False
    if cooldown_until and now < cooldown_until:
        cooldown = True
    return render_template('game_detail.html', game=game, attempts=attempts, max_attempts=max_attempts, cooldown=cooldown)

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_msg = data.get('message', '').strip()
    # Lógica simple: eco o respuesta programada
    if not user_msg:
        return jsonify({'response': '¿Puedes escribir tu pregunta?'}), 200
   
    if 'hola' in user_msg.lower():
        return jsonify({'response': '¡Hola! ¿En qué puedo ayudarte hoy?'}), 200
    if 'nivel' in user_msg.lower():
        return jsonify({'response': 'Puedes subir de nivel completando retos y juegos.'}), 200
    if 'juego' in user_msg.lower():
        return jsonify({'response': 'Para jugar, ve a la sección de Juegos y elige uno.'}), 200
    # Eco por defecto
    return jsonify({'response': f'Recibí: {user_msg}'}), 200


@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz_attempt(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    quiz = Quiz.query.get_or_404(quiz_id)
    # Obtener preguntas del quiz
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    if not questions:
        flash('Este quiz no tiene preguntas aún.')
        return redirect(url_for('dashboard'))
    max_attempts = 3
    cooldown_minutes = 30
    session_key = f'quiz_{quiz_id}_attempts'
    session_cooldown_key = f'quiz_{quiz_id}_cooldown'
    attempts = session.get(session_key, 0)
    cooldown_until = session.get(session_cooldown_key)
    import time
    now = int(time.time())
    if cooldown_until and now < cooldown_until:
        mins_left = int((cooldown_until - now) / 60) + 1
        return render_template('quiz.html', quiz=quiz, questions=questions, attempts=max_attempts, max_attempts=max_attempts, cooldown=True, mins_left=mins_left)
    if cooldown_until and now >= cooldown_until:
        attempts = 0
        session[session_key] = 0
        session.pop(session_cooldown_key, None)
    if attempts >= max_attempts:
        session[session_cooldown_key] = now + cooldown_minutes * 60
        mins_left = cooldown_minutes
        return render_template('quiz.html', quiz=quiz, questions=questions, attempts=max_attempts, max_attempts=max_attempts, cooldown=True, mins_left=mins_left)
    if request.method == 'POST':
        correctas = 0
        total = len(questions)
        user_answers = {}
        for q in questions:
            selected = request.form.get(f'q_{q.id}')
            user_answers[q.id] = selected
            is_correct = selected == q.correct_answer
            # Guardar respuesta
            answer = UserAnswer(
                user_id=user.id,
                question_id=q.id,
                selected_answer=selected,
                is_correct=is_correct,
                answered_at=datetime.utcnow()
            )
            db.session.add(answer)
            if is_correct:
                correctas += 1
        db.session.commit()
        results = [(q, user_answers.get(q.id)) for q in questions]
        if correctas == total:
            # Respuestas correctas, sumar puntos y resetear intentos
            # Si el quiz es de profesor, 15 puntos por pregunta, si no, 10
            puntos = 15 * total if quiz.teacher_id else 10 * total
            user.points += puntos
            db.session.commit()
            session[session_key] = 0
            session.pop(session_cooldown_key, None)
            show_15pts_modal = True
            return render_template('quiz.html', quiz=quiz, questions=questions, show_answers=True, results=results, attempts=0, max_attempts=max_attempts, show_15pts_modal=show_15pts_modal)
        else:
            # Respuestas incorrectas, aumentar intentos
            attempts += 1
            session[session_key] = attempts
            if attempts >= max_attempts:
                session[session_cooldown_key] = now + cooldown_minutes * 60
                mins_left = cooldown_minutes
                return render_template('quiz.html', quiz=quiz, questions=questions, attempts=max_attempts, max_attempts=max_attempts, cooldown=True, mins_left=mins_left)
            return render_template('quiz.html', quiz=quiz, questions=questions, attempts=attempts, max_attempts=max_attempts, error=True)
    return render_template('quiz.html', quiz=quiz, questions=questions, attempts=attempts, max_attempts=max_attempts)

@app.route('/admin/add_question', methods=['POST'])
def add_question():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    quiz_id = request.form['quiz_id']
    text = request.form['question_text'].strip()
    options = [
        request.form['option1'].strip(),
        request.form['option2'].strip(),
        request.form['option3'].strip(),
        request.form['option4'].strip()
    ]
    correct_index = int(request.form['correct_answer']) - 1
    if not text or any(not o for o in options) or correct_index not in range(4):
        flash('Todos los campos son obligatorios y la respuesta debe ser válida.')
        return redirect(url_for('admin_panel'))
    correct_answer = options[correct_index]
    new_question = Question(
        quiz_id=quiz_id,
        text=text,
        options=options,
        correct_answer=correct_answer
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Pregunta agregada correctamente.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/create_or_update_user', methods=['POST'])
def create_or_update_user():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user_id = request.form.get('user_id')
    username = request.form['username'].strip()
    email = request.form['email'].strip()
    area = request.form['area'].strip()
    points = int(request.form.get('points', 0))
    level = int(request.form.get('level', 1))
    password = request.form.get('password')
    if user_id:
        user = User.query.get(user_id)
        if not user:
            flash('Usuario no encontrado.')
            return redirect(url_for('admin_panel'))
        user.username = username
        user.email = email
        user.area = area
        user.points = points
        user.level = level
        if password:
            user.password = generate_password_hash(password)
        db.session.commit()
        flash('Usuario actualizado correctamente.')
    else:
        if not password:
            flash('La contraseña es obligatoria para crear un usuario.')
            return redirect(url_for('admin_panel'))
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe.')
            return redirect(url_for('admin_panel'))
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado.')
            return redirect(url_for('admin_panel'))
        new_user = User(
            username=username,
            email=email,
            area=area,
            points=points,
            level=level,
            password=generate_password_hash(password),
            is_admin=False
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Usuario creado correctamente.')
    session.pop('user_to_edit', None)
    return redirect(url_for('admin_panel'))

# Editar usuario (cargar en formulario)
@app.route('/admin/edit_user/<int:user_id>', methods=['GET'])
def edit_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user = User.query.get_or_404(user_id)
    session['user_to_edit'] = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'area': user.area,
        'points': user.points,
        'level': user.level
    }
    return redirect(url_for('admin_panel'))

# Cancelar edición de usuario
@app.route('/admin/clear_user_edit')
def clear_user_edit():
    session.pop('user_to_edit', None)
    return redirect(url_for('admin_panel'))

# Eliminar usuario
@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    # No permitir eliminar administradores
    if user.is_admin:
        flash('No se puede eliminar un usuario administrador.')
        return redirect(url_for('admin_panel'))
    
    # Eliminar datos relacionados del usuario
    UserAnswer.query.filter_by(user_id=user_id).delete()
    Achievement.query.filter_by(user_id=user_id).delete()
    # Notification.to_user is an Integer FK to users.id — use id, not username
    Notification.query.filter_by(to_user=user.id).delete()
    
    # Eliminar el usuario
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuario "{user.username}" eliminado correctamente.')
    return redirect(url_for('admin_panel'))

# Bloquear/Desbloquear usuario
@app.route('/admin/toggle_block_user/<int:user_id>', methods=['POST'])
def toggle_block_user(user_id):
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    
    # No permitir bloquear administradores
    if user.is_admin:
        flash('No se puede bloquear un usuario administrador.')
        return redirect(url_for('admin_panel'))
    
    # Cambiar estado de bloqueo
    user.is_blocked = not user.is_blocked
    db.session.commit()
    
    status = "bloqueado" if user.is_blocked else "desbloqueado"
    flash(f'Usuario "{user.username}" {status} correctamente.')
    return redirect(url_for('admin_panel'))

@app.route('/admin/assign_achievement', methods=['POST'])
def assign_achievement():
    if 'user_id' not in session or not session.get('is_admin'):
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user_id = request.form.get('user_id')
    badge_id = request.form.get('badge_id')
    if not user_id or not badge_id:
        flash('Usuario y logro requeridos.')
        return redirect(url_for('admin_panel'))
    # Evitar duplicados
    exists = Achievement.query.filter_by(user_id=user_id, badge_id=badge_id).first()
    if exists:
        flash('El usuario ya tiene este logro.')
        return redirect(url_for('admin_panel'))
    achievement = Achievement(user_id=user_id, badge_id=badge_id)
    db.session.add(achievement)
    db.session.commit()
    flash('Logro asignado correctamente.')
    return redirect(url_for('admin_panel'))

@app.route('/teacher/dashboard', methods=['GET', 'POST'])
def teacher_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    from models import Game
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher:
        flash('No tienes perfil de profesor.')
        return redirect(url_for('dashboard'))
    quizzes = Quiz.query.filter_by(teacher_id=teacher.id).all()
    games = Game.query.filter_by(teacher_id=teacher.id).all()
    badges = Badge.query.all()
    achievements = Achievement.query.filter(Achievement.badge_id.in_([b.id for b in badges])).all()
    notifications = Notification.query.filter_by(to_user=user.id).order_by(Notification.date_sent.desc()).limit(10).all()

    # Alumnos inscritos al área del profesor
    students = User.query.filter_by(area=teacher.area, is_admin=False).all()

    # Puntajes de los alumnos en quizzes y juegos creados por el profesor
    quiz_ids = [q.id for q in quizzes]
    game_ids = [g.id for g in games]
    student_scores = []
    for student in students:
        quiz_points = 0
        if quiz_ids:
                quiz_points = db.session.query(
                    db.func.sum(
                        db.case((UserAnswer.is_correct == True, 10), else_=0)
                    )
                ).join(Question).filter(
                    UserAnswer.user_id==student.id,
                    Question.quiz_id.in_(quiz_ids)
                ).scalar() or 0
        student_scores.append({
            'student': student,
            'quiz_points': quiz_points
        })

    ia_questions = None
    ia_tema = None
    if request.method == 'POST' and 'tema' in request.form and 'cantidad' in request.form:
        tema = request.form['tema']
        cantidad = int(request.form['cantidad'])
        ia_tema = tema
        tipo_examen = request.form.get('tipo_examen', 'simple')  # 'simple' o 'opciones'
        ia_questions = None
        try:
            import openai
            openai.api_key = os.getenv('OPENAI_API_KEY')
            if tipo_examen == 'opciones':
                prompt = (
                    f"Genera {cantidad} preguntas de opción múltiple para un examen de nivel medio superior sobre el tema '{tema}' del área de {teacher.area}. "
                    "Para cada pregunta, proporciona 4 opciones (a, b, c, d) y especifica la respuesta correcta. El formato debe ser:\n"
                    "1. Pregunta\n"
                    "a) Opción 1\n"
                    "b) Opción 2\n"
                    "c) Opción 3\n"
                    "d) Opción 4\n"
                    "Respuesta correcta: ...\n"
                    "Hazlo en español."
                )
            else:
                prompt = (
                    f"Genera {cantidad} preguntas para un examen de nivel medio superior sobre el tema '{tema}' del área de {teacher.area}. "
                    "Da solo la pregunta, sin respuestas ni opciones, en español."
                )
            # Usar la API moderna de OpenAI (chat.completions.create)
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": "Eres un generador de exámenes experto."},
                          {"role": "user", "content": prompt}],
                max_tokens=512 * cantidad,
                temperature=0.7
            )
            text = response.choices[0].message.content.strip()
            import re
            if tipo_examen == 'opciones':
                # Procesar preguntas con opciones y respuesta correcta
                preguntas = re.split(r'\n(?=\d+\.)', text)
                ia_questions = []
                for p in preguntas:
                    p = p.strip()
                    if not p:
                        continue
                    # Extraer pregunta, opciones y respuesta
                    m = re.match(r'(\d+\.\s*)(.*?)(?:\n|$)', p)
                    if m:
                        pregunta = m.group(2).strip()
                        resto = p[m.end():].strip()
                        opciones = re.findall(r'([a-d]\))\s*(.*)', resto)
                        opciones_texto = [opt[1].strip() for opt in opciones]
                        respuesta = re.search(r'Respuesta correcta\s*[:：]\s*(.*)', resto)
                        respuesta_texto = respuesta.group(1).strip() if respuesta else ''
                        ia_questions.append({
                            'pregunta': pregunta,
                            'opciones': opciones_texto,
                            'respuesta': respuesta_texto
                        })
                    else:
                        ia_questions.append({'pregunta': p, 'opciones': [], 'respuesta': ''})
            else:
                # Preguntas simples
                ia_questions = re.split(r'\n\d+\.\s*', text)
                ia_questions = [q.strip() for q in ia_questions if q.strip()]
                if len(ia_questions) < cantidad:
                    ia_questions = [q.strip() for q in text.split('\n') if q.strip()]
        except Exception as e:
            ia_questions = [f"Error generando preguntas: {e}"]

    return render_template('teacher_dashboard.html',
                           user=user,
                           teacher=teacher,
                           quizzes=quizzes,
                           games=games,
                           badges=badges,
                           achievements=achievements,
                           notifications=notifications,
                           students=students,
                           student_scores=student_scores,
                           ia_questions=ia_questions,
                           ia_tema=ia_tema,
                           ia_tipo_examen=request.form.get('tipo_examen', 'simple'))

# === NUEVAS RUTAS PARA PROFESOR ===
@app.route('/teacher/create_quiz', methods=['POST'])
def teacher_create_quiz():
    if 'user_id' not in session:
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher:
        flash('No tienes perfil de profesor.')
        return redirect(url_for('dashboard'))
    title = request.form['title'].strip()
    area = request.form['area'].strip()
    if not title or not area:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('teacher_dashboard'))
    new_quiz = Quiz(
        title=title,
        area=area,
        description=request.form.get('description', ''),
        created_by=user.id,
        teacher_id=teacher.id,
        created_at=datetime.utcnow()
    )
    db.session.add(new_quiz)
    db.session.commit()
    flash('Quiz creado correctamente.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/create_game', methods=['POST'])
def teacher_create_game():
    if 'user_id' not in session:
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher:
        flash('No tienes perfil de profesor.')
        return redirect(url_for('dashboard'))
    name = request.form.get('name', '').strip()
    type_ = request.form.get('type', '').strip()
    if not name or not type_:
        flash('Todos los campos son obligatorios.')
        return redirect(url_for('teacher_dashboard'))
    from models import Game
    new_game = Game(name=name, type=type_, teacher_id=teacher.id, created_at=datetime.utcnow())
    db.session.add(new_game)
    db.session.commit()
    flash('Juego creado correctamente.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/add_question', methods=['POST'])
def teacher_add_question():
    if 'user_id' not in session:
        flash('Acceso restringido.')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher:
        flash('No tienes perfil de profesor.')
        return redirect(url_for('dashboard'))
    quiz_id = request.form['quiz_id']
    text = request.form['question_text'].strip()
    options = [
        request.form['option1'].strip(),
        request.form['option2'].strip(),
        request.form['option3'].strip(),
        request.form['option4'].strip()
    ]
    correct_index = int(request.form['correct_answer']) - 1
    if not text or any(not o for o in options) or correct_index not in range(4):
        flash('Todos los campos son obligatorios y la respuesta debe ser válida.')
        return redirect(url_for('teacher_dashboard'))
    correct_answer = options[correct_index]
    quiz = Quiz.query.get(quiz_id)
    if not quiz or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para agregar preguntas a este quiz.')
        return redirect(url_for('teacher_dashboard'))
    new_question = Question(
        quiz_id=quiz_id,
        text=text,
        options=options,
        correct_answer=correct_answer
    )
    db.session.add(new_question)
    db.session.commit()
    flash('Pregunta agregada correctamente.')
    return redirect(url_for('teacher_dashboard'))
# Descargar examen en Word
@app.route('/download_exam_word', methods=['POST'])
def download_exam_word():
    from flask import send_file
    from io import BytesIO
    from docx import Document
    import json
    tema = request.form.get('tema', 'Examen')
    area = request.form.get('area', 'General')
    tipo_examen = request.form.get('tipo_examen', 'simple')
    preguntas_raw = request.form.get('preguntas', '')
    try:
        preguntas = json.loads(preguntas_raw)
    except Exception:
        preguntas = preguntas_raw.split('||') if preguntas_raw else []
    doc = Document()
    doc.add_heading(f'Examen de {area}', 0)
    doc.add_paragraph(f'Tema: {tema}')
    doc.add_paragraph('Instrucciones: Responde las siguientes preguntas.')
    if tipo_examen == 'opciones' and preguntas and isinstance(preguntas[0], dict):
        for i, q in enumerate(preguntas, 1):
            doc.add_paragraph(f'{i}. {q.get("pregunta", "")}', style='List Number')
            for idx, opt in enumerate(q.get('opciones', [])):
                doc.add_paragraph(f"    {chr(97+idx)}) {opt}", style=None)
            doc.add_paragraph(f"Respuesta correcta: {q.get('respuesta','')}", style=None)
    else:
        for i, q in enumerate(preguntas, 1):
            doc.add_paragraph(f'{i}. {q}', style='List Number')
    f = BytesIO()
    doc.save(f)
    f.seek(0)
    filename = f"Examen_{area}_{tema}.docx".replace(' ', '_')
    return send_file(f, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

# Descargar examen en PDF
@app.route('/download_exam_pdf', methods=['POST'])
def download_exam_pdf():
    from flask import send_file
    from io import BytesIO
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    import json
    tema = request.form.get('tema', 'Examen')
    area = request.form.get('area', 'General')
    tipo_examen = request.form.get('tipo_examen', 'simple')
    preguntas_raw = request.form.get('preguntas', '')
    try:
        preguntas = json.loads(preguntas_raw)
    except Exception:
        preguntas = preguntas_raw.split('||') if preguntas_raw else []
    f = BytesIO()
    c = canvas.Canvas(f, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica-Bold', 16)
    c.drawString(40, height-50, f'Examen de {area}')
    c.setFont('Helvetica', 12)
    c.drawString(40, height-80, f'Tema: {tema}')
    c.drawString(40, height-100, 'Instrucciones: Responde las siguientes preguntas.')
    y = height-130
    if tipo_examen == 'opciones' and preguntas and isinstance(preguntas[0], dict):
        for i, q in enumerate(preguntas, 1):
            c.drawString(40, y, f'{i}. {q.get("pregunta", "")}')
            y -= 20
            for idx, opt in enumerate(q.get('opciones', [])):
                c.drawString(60, y, f"{chr(97+idx)}) {opt}")
                y -= 18
            c.drawString(60, y, f"Respuesta correcta: {q.get('respuesta','')}")
            y -= 25
            if y < 60:
                c.showPage()
                y = height-50
    else:
        for i, q in enumerate(preguntas, 1):
            c.drawString(40, y, f'{i}. {q}')
            y -= 25
            if y < 60:
                c.showPage()
                y = height-50
    c.save()
    f.seek(0)
    filename = f"Examen_{area}_{tema}.pdf".replace(' ', '_')
    return send_file(f, as_attachment=True, download_name=filename, mimetype='application/pdf')


@app.route('/teacher/editar_quiz/<int:quiz_id>', methods=['GET', 'POST'])
def editar_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    quiz = Quiz.query.get_or_404(quiz_id)
    # Solo permitir editar si el usuario es el profesor creador
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para editar este quiz.')
        return redirect(url_for('teacher_dashboard'))
    if request.method == 'POST':
        quiz.title = request.form['title'].strip()
        quiz.area = request.form['area'].strip()
        quiz.description = request.form.get('description', '').strip()
        db.session.commit()
        flash('Quiz actualizado correctamente.')
        return redirect(url_for('teacher_dashboard'))
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/teacher/eliminar_quiz/<int:quiz_id>', methods=['POST'])
def eliminar_quiz(quiz_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    quiz = Quiz.query.get_or_404(quiz_id)
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para eliminar este quiz.')
        return redirect(url_for('teacher_dashboard'))
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz eliminado correctamente.')
    return redirect(url_for('teacher_dashboard'))

@app.route('/teacher/editar_juego/<int:game_id>', methods=['GET', 'POST'])
def editar_juego(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    from models import Game
    game = Game.query.get_or_404(game_id)
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or game.teacher_id != teacher.id:
        flash('No tienes permisos para editar este juego.')
        return redirect(url_for('teacher_dashboard'))
    if request.method == 'POST':
        game.name = request.form['name'].strip()
        game.description = request.form['description'].strip()
        game.type = request.form['type'].strip()
        game.rules = request.form['rules'].strip()
        db.session.commit()
        flash('Juego actualizado correctamente.')
        return redirect(url_for('teacher_dashboard'))
    return render_template('edit_game.html', game=game)

@app.route('/teacher/eliminar_juego/<int:game_id>', methods=['POST'])
def eliminar_juego(game_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    from models import Game
    game = Game.query.get_or_404(game_id)
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or game.teacher_id != teacher.id:
        flash('No tienes permisos para eliminar este juego.')
        return redirect(url_for('teacher_dashboard'))
    db.session.delete(game)
    db.session.commit()
    flash('Juego eliminado correctamente.')
    return redirect(url_for('teacher_dashboard'))

# Editar pregunta (profesor)
@app.route('/teacher/editar_pregunta/<int:question_id>', methods=['GET', 'POST'])
def editar_pregunta(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get(question.quiz_id)
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para editar esta pregunta.')
        return redirect(url_for('teacher_dashboard'))
    if request.method == 'POST':
        question.text = request.form['question_text'].strip()
        question.options = [
            request.form['option1'].strip(),
            request.form['option2'].strip(),
            request.form['option3'].strip(),
            request.form['option4'].strip()
        ]
        correct_index = int(request.form['correct_answer']) - 1
        if correct_index not in range(4):
            flash('La respuesta correcta debe ser válida.')
            return redirect(url_for('editar_pregunta', question_id=question.id))
        question.correct_answer = question.options[correct_index]
        db.session.commit()
        flash('Pregunta actualizada correctamente.')
        return redirect(url_for('teacher_dashboard'))
    return render_template('edit_question.html', question=question)

# Eliminar pregunta (profesor)
@app.route('/teacher/eliminar_pregunta/<int:question_id>', methods=['POST'])
def eliminar_pregunta(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get(question.quiz_id)
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if not teacher or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para eliminar esta pregunta.')
        return redirect(url_for('teacher_dashboard'))
    db.session.delete(question)
    db.session.commit()
    flash('Pregunta eliminada correctamente.')
    return redirect(url_for('teacher_dashboard'))

# Editar pregunta (profesor)
@app.route('/teacher/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    question = Question.query.get_or_404(question_id)
    quiz = Quiz.query.get(question.quiz_id)
    if not teacher or quiz.teacher_id != teacher.id:
        flash('No tienes permisos para editar esta pregunta.')
        return redirect(url_for('teacher_dashboard'))
    if request.method == 'POST':
        text = request.form['question_text'].strip()
        options = [
            request.form['option1'].strip(),
            request.form['option2'].strip(),
            request.form['option3'].strip(),
            request.form['option4'].strip()
        ]
        correct_index = int(request.form['correct_answer']) - 1
        if not text or any(not o for o in options) or correct_index not in range(4):
            flash('Todos los campos son obligatorios y la respuesta debe ser válida.')
            return render_template('edit_question.html', question=question)
        question.text = text
        question.options = options
        question.correct_answer = options[correct_index]
        db.session.commit()
        flash('Pregunta actualizada correctamente.')
        return redirect(url_for('teacher_dashboard'))
    return render_template('edit_question.html', question=question)

if __name__ == '__main__':
    socketio.run(app, debug=True)
