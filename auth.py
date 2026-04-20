from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from models import User, db
from utils import get_user_by_username, get_user_by_email, create_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return redirect(url_for('auth.register'))

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('auth.register'))

        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.register'))

        # Create user
        user, message = create_user(username, email, password)
        if not user:
            flash(message, 'danger')
            return redirect(url_for('auth.register'))

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login user"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth.login'))

        user = get_user_by_username(username)
        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Your account is disabled.', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))


@auth_bp.route('/api/auth/verify')
def verify_auth():
    """Check if user is authenticated (API endpoint)"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'username': current_user.username,
            'is_admin': current_user.is_admin()
        })
    return jsonify({'authenticated': False})
