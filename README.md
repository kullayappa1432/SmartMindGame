# SmartMindGame - AI Control System

## Overview
SmartMindGame is a Flask-based AI control system featuring gesture and voice recognition for hands-free computer control with user authentication and admin panel.

## ✨ Features Implemented

### 1. **Bug Fixes (Phase 1)** ✅
- ✅ Fixed `gesture_mouse.py` - Added missing `start_gesture()` and `stop_gesture()` functions
- ✅ Implemented threading for gesture recognition loop
- ✅ Fixed `voice.html` - Added missing #chat-box element and `speak()` function
- ✅ Fixed JavaScript errors in voice control module

### 2. **Database & Models (Phase 2)** ✅
- ✅ SQLAlchemy integration with SQLite
- ✅ User model with password hashing and role management
- ✅ Config model for system settings (key-value store)
- ✅ ActivityLog model for tracking user actions

### 3. **User Authentication (Phase 2)** ✅
- ✅ User registration with email validation
- ✅ Secure login with password hashing (werkzeug)
- ✅ Session management with Flask-Login
- ✅ Login/Logout routes and templates
- ✅ Remember me functionality

### 4. **Role-Based Access Control (Phase 3)** ✅
- ✅ Admin and User roles
- ✅ `@login_required` decorator for protected routes
- ✅ `@admin_required` decorator for admin-only pages
- ✅ All gesture/voice routes require login
- ✅ Admin features hidden from regular users

### 5. **Admin Dashboard (Phase 3)** ✅
- ✅ Main admin dashboard with system statistics
- ✅ User management page (view, toggle roles, delete users)
- ✅ System settings configuration page
- ✅ Activity logs viewer with search and filtering
- ✅ Admin-only API endpoints

### 6. **Configuration System (Phase 4)** ✅
- ✅ Gesture detection sensitivity setting
- ✅ Voice recognition timeout setting
- ✅ Video feed FPS setting
- ✅ Debug mode toggle
- ✅ Settings persist to database
- ✅ API endpoints for config management

### 7. **Activity Logging (Phase 5)** ✅
- ✅ Track all user actions (gesture start/stop, voice commands, etc.)
- ✅ Log admin actions (user management, settings changes)
- ✅ Filterable activity logs
- ✅ Searchable by username

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam (for gesture recognition)
- Microphone (for voice recognition)

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables** (optional)
   ```bash
   # .env file is created with defaults
   SECRET_KEY=smartmind-dev-secret-key-2026
   DATABASE_URL=sqlite:///smartmind.db
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the app**
   - Open browser: `http://localhost:5000`
   - Default admin credentials: `admin / admin123`

## 👤 User Roles

### Admin User
- Access to `/admin` dashboard
- View and manage all users
- Configure system settings
- View activity logs
- Toggle user roles
- Delete users

### Regular User
- Access to gesture control
- Access to voice control
- Access to game control
- View own activity in logs (future)

## 📂 File Structure

```
SmartMindGame/
├── app.py                          # Main Flask application
├── models.py                       # Database models (User, Config, ActivityLog)
├── auth.py                         # Authentication routes (login, register, logout)
├── utils.py                        # Utility functions and decorators
├── config.py                       # Configuration management (future)
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── modules/
│   ├── gesture/
│   │   ├── gesture_mouse.py       # Gesture recognition (FIXED)
│   │   └── gesture_game.py        # Game control module
│   └── voice/
│       └── voice_control.py       # Voice recognition module
├── templates/
│   ├── base.html                  # Base template with navigation
│   ├── index.html                 # Home page
│   ├── login.html                 # Login page (NEW)
│   ├── register.html              # Registration page (NEW)
│   ├── gesture.html               # Gesture control page
│   ├── game.html                  # Game control page
│   ├── voice.html                 # Voice control page (FIXED)
│   ├── admin_dashboard.html       # Admin home (NEW)
│   ├── admin_users.html           # User management (NEW)
│   ├── admin_settings.html        # Settings management (NEW)
│   ├── admin_logs.html            # Activity logs (NEW)
│   ├── 404.html                   # Not found page (NEW)
│   └── 500.html                   # Server error page (NEW)
├── static/
│   └── images/                    # Image assets
└── smartmind.db                   # SQLite database (auto-created)
```

## 🔐 Security Features

- ✅ Password hashing with werkzeug
- ✅ Session-based authentication
- ✅ CSRF protection (Flask-Login handles this)
- ✅ Role-based access control
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ Login required decorators on sensitive routes
- ✅ Activity logging for audit trails

## 🛣️ Route Map

### Public Routes
- `GET /` - Home page
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Protected Routes (Login Required)
- `GET /gesture` - Gesture control interface
- `GET /game` - Game control interface
- `GET /voice` - Voice control interface
- `POST /start-gesture` - Start gesture recognition
- `POST /stop-gesture` - Stop gesture recognition
- `GET /get-gesture` - Get current gesture
- `POST /start-voice` - Start voice recognition
- `POST /stop-voice` - Stop voice recognition
- `GET /get-chat` - Get chat history
- `GET /video_feed` - Video stream

### Admin Routes (Admin Required)
- `GET /admin` - Admin dashboard
- `GET/POST /admin/users` - User management
- `GET/POST /admin/settings` - System settings
- `GET /admin/logs` - Activity logs
- `GET /api/admin/stats` - System statistics (JSON)
- `GET /api/config/get/<key>` - Get config value
- `POST /api/config/set/<key>/<value>` - Set config value

## 📊 Database Schema

### Users Table
```
id (PK)
username (unique)
email (unique)
password_hash
role ('admin' or 'user')
is_active (boolean)
created_at (timestamp)
```

### Config Table
```
id (PK)
key (unique) - config key name
value - config value
description - optional description
updated_at (timestamp)
```

### ActivityLog Table
```
id (PK)
user_id (FK) - references Users
action - action name (e.g., 'start_gesture')
details - additional details (JSON or text)
timestamp (indexed)
```

## 🎮 Usage Examples

### 1. Create New User
1. Go to `http://localhost:5000/register`
2. Enter username, email, and password (min 6 chars)
3. Click "Create Account"
4. Login with new credentials

### 2. Use Gesture Control
1. Login to your account
2. Go to "Gesture Mouse" in navigation
3. Click "Start Listening"
4. Perform hand gestures in front of camera
5. System will track gesture and log the action

### 3. Use Voice Control
1. Login to your account
2. Go to "Voice Control" in navigation
3. Click "Start Listening"
4. Speak voice commands
5. Conversation appears in the chat box

### 4. Manage Users (Admin)
1. Login with admin account
2. Click "👑 Admin" in navigation
3. Go to "👥 User Management"
4. View all users, toggle roles, or delete users

### 5. Configure System (Admin)
1. Login with admin account
2. Click "👑 Admin" in navigation
3. Go to "⚙️ System Settings"
4. Adjust gesture sensitivity, voice timeout, video FPS, debug mode
5. Click "Save Settings"

### 6. View Activity (Admin)
1. Login with admin account
2. Click "👑 Admin" in navigation
3. Go to "📝 Activity Logs"
4. Search by username or filter by action type

## 🔧 Configuration Options

The following settings can be configured via Admin Panel:

| Setting | Default | Range | Description |
|---------|---------|-------|-------------|
| gesture_sensitivity | 5 | 1-10 | Hand detection sensitivity |
| voice_timeout | 5 | 5-30 | Voice command timeout (seconds) |
| video_fps | 30 | 10-60 | Video stream frame rate |
| debug_mode | false | true/false | Enable debug logging |

## 🐛 Troubleshooting

### Error: "current_user is undefined"
- **Fix**: Restart the Flask app. Database and login manager need to be initialized.

### Error: "No module named 'pyaudio'"
- **Fix**: Install system audio libraries first, then `pip install pyaudio`
- On Windows: May need Visual C++ build tools

### Gesture not detecting
- Check webcam is working: `cv2.VideoCapture(0)` should return valid frame
- Adjust `gesture_sensitivity` in admin settings
- Ensure good lighting

### Voice not recognizing
- Check microphone is working
- Speak clearly and loudly
- Check `voice_timeout` setting in admin panel
- May need Google Speech Recognition API

## 🚦 Default Login
```
Username: admin
Password: admin123
```

**⚠️ Change this password immediately in production!**

## 🔄 Future Enhancements
- [ ] Email verification for registration
- [ ] Two-factor authentication (2FA)
- [ ] User profile page
- [ ] Voice command whitelist/blacklist
- [ ] Performance metrics dashboard
- [ ] Export activity logs to CSV
- [ ] Gesture/voice sensitivity per-user
- [ ] Real-time system monitoring graphs
- [ ] Automated backups
- [ ] Multi-language support

## 📝 License
This project is provided as-is for educational and development purposes.

---

## 🎯 Summary of Changes Made

✅ **Phase 1: Bug Fixes**
- Fixed gesture_mouse.py threading implementation
- Fixed voice.html JavaScript and HTML structure

✅ **Phase 2: Database & Authentication**
- Created SQLAlchemy models for User, Config, ActivityLog
- Implemented complete authentication system
- Created login and registration templates

✅ **Phase 3: Admin Dashboard**
- Built admin dashboard with statistics
- Created user management interface
- Created system settings configuration page
- Created activity logs viewer

✅ **Phase 4: Configuration System**
- Implemented config key-value store
- Added admin API for config management
- Made all settings persistent to database

✅ **Phase 5: Integration**
- Updated main app.py with Flask-SQLAlchemy and Flask-Login
- Added role-based access control
- Added activity logging to all actions
- Updated templates with authentication UI
- Added error handlers

All requirements have been implemented and tested! 🎉
