from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """User model for authentication and role management"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'admin' or 'user'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'


class Config(db.Model):
    """System configuration key-value store"""
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Config {self.key}={self.value}>'


class ActivityLog(db.Model):
    """Activity log for tracking user actions"""
    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    action = db.Column(db.String(200), nullable=False)  # e.g., 'start_gesture', 'voice_command'
    details = db.Column(db.Text)  # JSON or text details
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<ActivityLog {self.user_id} - {self.action}>'


class PasswordReset(db.Model):
    """Password reset tokens and OTP for forgot password flow"""
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    otp = db.Column(db.String(6), nullable=False)  # 6-digit OTP
    reset_token = db.Column(db.String(100), unique=True, nullable=False, index=True)  # For security
    email = db.Column(db.String(120), nullable=False)  # Email to verify
    is_verified = db.Column(db.Boolean, default=False)  # OTP verified?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=30))
    
    user = db.relationship('User', backref='password_resets')
    
    def is_expired(self):
        """Check if OTP has expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is still valid and not verified"""
        return not self.is_expired() and not self.is_verified
    
    @staticmethod
    def generate_otp():
        """Generate a random 6-digit OTP"""
        import random
        return ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    @staticmethod
    def generate_token():
        """Generate a secure reset token"""
        return secrets.token_urlsafe(32)
    
    def __repr__(self):
        return f'<PasswordReset {self.user_id} - {self.email}>'
