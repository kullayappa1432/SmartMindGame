from flask import Flask, render_template, Response, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_required
import cv2
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ✅ IMPORT CORRECT FUNCTIONS
from modules.voice.voice_control import start_voice, stop_voice, get_chat
from modules.gesture.gesture_mouse import (
    start_gesture,
    stop_gesture,
    get_gesture,
    get_frame
)

# Database & Auth imports
from models import db, User, Config, ActivityLog
from auth import auth_bp
from routes.game_routes import game_bp
from utils import admin_required, log_activity, get_system_stats, toggle_user_role, delete_user

app = Flask(__name__)

# =========================
# ⚙️ CONFIGURATION
# =========================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///smartmind.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================
# 📦 INITIALIZE EXTENSIONS
# =========================
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# =========================
# 👤 LOAD USER
# =========================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# 📋 CONTEXT PROCESSORS
# =========================
@app.context_processor
def inject_user():
    return {'current_user': current_user}

# =========================
# 📝 REGISTER BLUEPRINTS
# =========================
app.register_blueprint(auth_bp)
app.register_blueprint(game_bp)

# =========================
# 📊 CREATE TABLES
# =========================
with app.app_context():
    db.create_all()

    # Create default admin if doesn't exist
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@smartmind.local', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # Add default config
        default_configs = [
            Config(key='gesture_sensitivity', value='5', description='Gesture detection sensitivity (1-10)'),
            Config(key='voice_timeout', value='5', description='Voice recognition timeout (seconds)'),
            Config(key='video_fps', value='30', description='Video feed FPS'),
            Config(key='debug_mode', value='false', description='Enable debug logging'),
        ]
        for config in default_configs:
            existing = Config.query.filter_by(key=config.key).first()
            if not existing:
                db.session.add(config)

        db.session.commit()
        print("[OK] Default admin created: admin/admin123")

# =========================
# 🎥 VIDEO STREAM (FIXED)
# =========================
def generate_frames():
    while True:
        frame = get_frame()

        if frame is None:
            time.sleep(0.01)
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# =========================
# 📄 PAGES
# =========================
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/gesture')
@login_required
def gesture_page():
    log_activity('view_gesture_page')
    return render_template('gesture.html')


@app.route('/game')
@login_required
def game():
    log_activity('view_game_page')
    return render_template('game.html')


@app.route('/voice')
@login_required
def voice():
    log_activity('view_voice_page')
    return render_template('voice.html')


# =========================
# ✋ GESTURE ROUTES
# =========================
@app.route('/start-gesture')
@login_required
def start_gesture_route():
    start_gesture()
    log_activity('start_gesture', 'Gesture recognition started')
    return jsonify({"status": "Gesture Started"})


@app.route('/stop-gesture')
@login_required
def stop_gesture_route():
    stop_gesture()
    log_activity('stop_gesture', 'Gesture recognition stopped')
    return jsonify({"status": "Gesture Stopped"})


@app.route('/get-gesture')
@login_required
def get_gesture_route():
    return jsonify({"gesture": get_gesture()})


# =========================
# 🎤 VOICE ROUTES
# =========================
@app.route('/start-voice')
@login_required
def start_voice_route():
    start_voice()
    log_activity('start_voice', 'Voice control started')
    return jsonify({"status": "Voice Started"})


@app.route('/stop-voice')
@login_required
def stop_voice_route():
    stop_voice()
    log_activity('stop_voice', 'Voice control stopped')
    return jsonify({"status": "Voice Stopped"})


@app.route('/get-chat')
@login_required
def chat():
    return jsonify({"chat": get_chat()})


# =========================
# 👑 ADMIN ROUTES
# =========================
@app.route('/admin')
@admin_required
def admin_dashboard():
    log_activity('view_admin_dashboard', 'Admin accessed dashboard')
    stats = get_system_stats()
    return render_template('admin_dashboard.html', stats=stats)


@app.route('/admin/users', methods=['GET', 'POST'])
@admin_required
def admin_users():
    if request.method == 'POST':
        action = request.form.get('action')
        user_id = request.form.get('user_id')

        if action == 'toggle_role':
            success, message = toggle_user_role(int(user_id))
            log_activity('toggle_user_role', f'User {user_id} role toggled')
            flash(message, 'success' if success else 'danger')

        elif action == 'delete':
            success, message = delete_user(int(user_id))
            log_activity('delete_user', f'User {user_id} deleted')
            flash(message, 'success' if success else 'danger')

        return redirect(url_for('admin_users'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)


@app.route('/admin/settings', methods=['GET', 'POST'])
@admin_required
def admin_settings():
    if request.method == 'POST':
        settings_to_update = {
            'gesture_sensitivity': request.form.get('gesture_sensitivity', '5'),
            'voice_timeout': request.form.get('voice_timeout', '5'),
            'video_fps': request.form.get('video_fps', '30'),
            'debug_mode': request.form.get('debug_mode', 'false'),
        }

        for key, value in settings_to_update.items():
            config = Config.query.filter_by(key=key).first()
            if config:
                config.value = value
            else:
                config = Config(key=key, value=value)
                db.session.add(config)

        db.session.commit()
        log_activity('update_settings', 'System settings updated')
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))

    # Get current settings
    settings = {}
    configs = Config.query.all()
    for config in configs:
        settings[config.key] = config.value

    return render_template('admin_settings.html', settings=settings)


@app.route('/admin/logs')
@admin_required
def admin_logs():
    search = request.args.get('search', '')
    action_filter = request.args.get('action_filter', '')

    query = ActivityLog.query

    if search:
        query = query.join(User).filter(User.username.ilike(f'%{search}%'))

    if action_filter:
        query = query.filter(ActivityLog.action == action_filter)

    logs = query.order_by(ActivityLog.timestamp.desc()).limit(100).all()

    return render_template('admin_logs.html', logs=logs, search=search, action_filter=action_filter)


# =========================
# 📊 API ENDPOINTS
# =========================
@app.route('/api/admin/stats')
@admin_required
def api_admin_stats():
    stats = get_system_stats()
    return jsonify(stats)


@app.route('/api/config/get/<key>')
@login_required
def api_config_get(key):
    config = Config.query.filter_by(key=key).first()
    if config:
        return jsonify({"key": key, "value": config.value})
    return jsonify({"error": "Config not found"}), 404


@app.route('/api/config/set/<key>/<value>', methods=['POST'])
@admin_required
def api_config_set(key, value):
    config = Config.query.filter_by(key=key).first()
    if config:
        config.value = value
        db.session.commit()
        log_activity('set_config', f'Config {key} set to {value}')
        return jsonify({"status": "OK"})
    return jsonify({"error": "Config not found"}), 404


# =========================
# ⚠️ ERROR HANDLERS
# =========================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(e):
    flash('Access denied.', 'danger')
    return redirect(url_for('home'))


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
