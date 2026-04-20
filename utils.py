from functools import wraps
from flask import redirect, url_for, flash, jsonify, g
from flask_login import current_user
from models import User, ActivityLog, db
from datetime import datetime


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        if not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def log_activity(action, details=None):
    """Log user activity to database"""
    if current_user.is_authenticated:
        log_entry = ActivityLog(
            user_id=current_user.id,
            action=action,
            details=details
        )
        db.session.add(log_entry)
        db.session.commit()


def get_user_by_username(username):
    """Get user by username"""
    return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Get user by email"""
    return User.query.filter_by(email=email).first()


def create_user(username, email, password, role='user'):
    """Create new user"""
    if get_user_by_username(username):
        return None, "Username already exists"
    if get_user_by_email(email):
        return None, "Email already exists"

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, "User created successfully"


def toggle_user_role(user_id):
    """Toggle user role between admin and user"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    user.role = 'user' if user.role == 'admin' else 'admin'
    db.session.commit()
    return True, f"User role changed to {user.role}"


def delete_user(user_id):
    """Delete user"""
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    db.session.delete(user)
    db.session.commit()
    return True, "User deleted"


def get_system_stats():
    """Get system statistics"""
    total_users = User.query.count()
    admin_users = User.query.filter_by(role='admin').count()
    recent_logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()

    return {
        'total_users': total_users,
        'admin_users': admin_users,
        'recent_activity': len(recent_logs)
    }
