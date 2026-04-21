from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user
from models import User, db, PasswordReset
from utils import get_user_by_username, get_user_by_email, create_user
from email_utils import send_otp_email, send_password_reset_confirmation

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


# ===================================
# 🔐 FORGOT PASSWORD ROUTES
# ===================================

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password - request OTP"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Email is required.', 'danger')
            return redirect(url_for('auth.forgot_password'))
        
        # Find user by email
        user = get_user_by_email(email)
        if not user:
            # Don't reveal if email exists (security best practice)
            flash('If an account exists with this email, you will receive an OTP.', 'info')
            return redirect(url_for('auth.login'))
        
        # Generate OTP and token
        otp = PasswordReset.generate_otp()
        reset_token = PasswordReset.generate_token()
        
        # Delete any existing reset requests for this user
        PasswordReset.query.filter_by(user_id=user.id).delete()
        db.session.commit()
        
        # Create new password reset record
        password_reset = PasswordReset(
            user_id=user.id,
            otp=otp,
            reset_token=reset_token,
            email=email,
            is_verified=False
        )
        
        try:
            db.session.add(password_reset)
            db.session.commit()
            
            # Send OTP email
            if send_otp_email(email, user.username, otp):
                flash('OTP has been sent to your email! Check your inbox.', 'success')
                # Redirect to verify OTP page with token
                return redirect(url_for('auth.verify_otp', token=reset_token))
            else:
                flash('Failed to send OTP. Please try again later.', 'danger')
                return redirect(url_for('auth.forgot_password'))
                
        except Exception as e:
            db.session.rollback()
            print(f"Error creating password reset: {str(e)}")
            flash('An error occurred. Please try again later.', 'danger')
            return redirect(url_for('auth.forgot_password'))
    
    return render_template('forgot_password.html')


@auth_bp.route('/verify-otp/<token>', methods=['GET', 'POST'])
def verify_otp(token):
    """Verify OTP"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Find password reset record by token
    password_reset = PasswordReset.query.filter_by(reset_token=token).first()
    
    if not password_reset:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if password_reset.is_expired():
        # Delete expired record
        db.session.delete(password_reset)
        db.session.commit()
        flash('Reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if not otp:
            flash('OTP is required.', 'danger')
            return redirect(url_for('auth.verify_otp', token=token))
        
        if otp != password_reset.otp:
            flash('Invalid OTP. Please try again.', 'danger')
            return redirect(url_for('auth.verify_otp', token=token))
        
        # Mark as verified
        password_reset.is_verified = True
        db.session.commit()
        
        flash('OTP verified! You can now reset your password.', 'success')
        return redirect(url_for('auth.reset_password', token=token))
    
    return render_template('verify_otp.html', token=token, email=password_reset.email)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password after OTP verification"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    # Find password reset record by token
    password_reset = PasswordReset.query.filter_by(reset_token=token).first()
    
    if not password_reset:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if not password_reset.is_verified:
        flash('Please verify your OTP first.', 'danger')
        return redirect(url_for('auth.verify_otp', token=token))
    
    if password_reset.is_expired():
        # Delete expired record
        db.session.delete(password_reset)
        db.session.commit()
        flash('Reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not password or not password_confirm:
            flash('Both password fields are required.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        
        if password != password_confirm:
            flash('Passwords do not match.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
        
        try:
            # Get user and update password
            user = password_reset.user
            user.set_password(password)
            
            # Delete password reset record
            db.session.delete(password_reset)
            db.session.commit()
            
            # Send confirmation email
            send_password_reset_confirmation(user.email, user.username)
            
            flash('Password has been reset successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting password: {str(e)}")
            flash('An error occurred. Please try again later.', 'danger')
            return redirect(url_for('auth.reset_password', token=token))
    
    return render_template('reset_password.html', token=token)
