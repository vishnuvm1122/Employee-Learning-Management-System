# 🎓 Employee Learning Management System (LMS)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.0+-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.x-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)

**🚀 Secure • 📚 Scalable • 🎯 Organized • 👨‍💼 Employee-Focused**

A comprehensive web-based Employee Learning Management System built with Python, Django, MySQL, Bootstrap, and JavaScript for managing employee training, courses, and learning activities.

[🚀 Quick Start](#-quick-start) • [📚 Features](#-features) • [🏗️ Architecture](#-architecture) • [📖 Documentation](#-documentation)

</div>

---

## 📺 Demo Video

<div align="center">

[![Employee LMS Demo](https://img.shields.io/badge/▶️%20Watch%20Demo-Video%20Walkthrough-blue?style=for-the-badge)](Screencast%202026-09-01%2012%3A01%3A52.mp4)

**[View Demo Video](Screencast%202026-09-01%2012%3A01%3A52.mp4)** - See the Employee LMS in action

</div>

---

## 📋 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Features](#-features)
- [🏗️ System Architecture](#-system-architecture)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Quick Start](#-quick-start)
- [📖 Detailed Installation](#-detailed-installation)
- [⚙️ Configuration](#-configuration)
- [🧪 Testing](#-testing)
- [📊 Database](#-database)
- [🔐 Security](#-security)
- [🩺 Troubleshooting](#-troubleshooting)
- [📝 Useful Commands](#-useful-commands)
- [🎯 Project Objectives](#-project-objectives)
- [🌟 Future Enhancements](#-future-enhancements)
- [📄 License](#-license)
- [🔗 Links](#-links)

---

## 🌟 Overview

The **Employee Learning Management System** is a centralized, secure platform designed to:

✅ Manage employee accounts and authentication  
✅ Create and organize training courses  
✅ Allocate courses to employees  
✅ Track learning progress and completion  
✅ Send automated notifications and reminders  
✅ Monitor security activities and suspicious logins  
✅ Manage email communications  
✅ Support mobile app integration (Android)  

**Perfect for:** Corporate training departments, HR teams, and organizations seeking centralized learning management.

---

## ✨ Features

### 👤 User Management
- ✅ Create, edit, and manage employee accounts
- ✅ Activate/deactivate user accounts
- ✅ Role-based access control
- ✅ User profile management

### 🔐 Authentication & Security
- ✅ Secure login/logout
- ✅ Session management
- ✅ Password reset workflow
- ✅ Two-factor authentication support
- ✅ Security monitoring
- ✅ Suspicious login detection
- ✅ Device & browser tracking
- ✅ IP address logging

### 📚 Course Management
- ✅ Create and organize training courses
- ✅ Add course descriptions and materials
- ✅ Set course prerequisites
- ✅ Manage course content
- ✅ Track course versions

### 🎯 Course Allocation
- ✅ Assign courses to employees
- ✅ Batch course allocation
- ✅ Set assignment deadlines
- ✅ Track allocation status

### 📊 Learning Progress
- ✅ Real-time progress tracking
- ✅ Completion status monitoring
- ✅ Learning analytics dashboard
- ✅ Performance reports
- ✅ Quiz management
- ✅ Result tracking

### 📧 Email & Notifications
- ✅ SMTP email configuration
- ✅ Automated password reset emails
- ✅ Course allocation notifications
- ✅ Daily learning reminders
- ✅ Weekly summary emails
- ✅ Suspicious login alerts
- ✅ In-app notifications

### 📅 Reminders & Scheduling
- ✅ Daily reminder emails
- ✅ Weekly summary notifications
- ✅ Deadline reminders
- ✅ Scheduled task automation

### 📱 Android Integration
- ✅ App version management
- ✅ APK release management
- ✅ Force update capabilities
- ✅ Download tracking

### 👨‍💼 Admin Dashboard
- ✅ Centralized management interface
- ✅ Quick statistics overview
- ✅ Activity logs
- ✅ System monitoring
- ✅ User engagement metrics

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     🌐 END USERS                                │
│              (Employees, Admins, Managers)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────▼──────────┐
                   │  🌍 WEB BROWSER    │
                   │ HTML5 • CSS3 • JS  │
                   │    Bootstrap       │
                   └─────────┬──────────┘
                             │
              ┌──────────────▼──────────────┐
              │  🔒 HTTPS / SSL              │
              └──────────────┬──────────────┘
                             │
            ┌────────────────▼────────────────┐
            │   🐍 DJANGO WEB FRAMEWORK       │
            │  (Backend Application Server)   │
            └─┬────────────┬─────────┬────────┘
              │            │         │
        ┌─────▼─┐    ┌────▼───┐ ┌──▼────┐
        │ 👤    │    │ 📚     │ │ 🛡️    │
        │ USER  │    │ COURSE │ │SECURITY
        │ MGMT  │    │ MGMT   │ │MONITOR
        └───────┘    └────────┘ └───────┘
              │            │         │
        ┌─────┴────────────┴─────────┴──────┐
        │                                    │
    ┌───▼────────┐                  ┌──────▼────┐
    │ 🗄️ MySQL   │                  │ 📧 SMTP   │
    │ Database   │                  │ Server    │
    │            │                  │           │
    │ • Users    │                  │Notifications
    │ • Courses  │                  │Emails
    │ • Progress │                  │Alerts
    │ • Security │                  │Reminders
    └────────────┘                  └───────────┘
```

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.x, Django 4.0+ |
| **Database** | MySQL 8.0+ |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **CSS Framework** | Bootstrap 5.x |
| **ORM** | Django ORM |
| **Authentication** | Django Authentication |
| **Email** | Django Email Backend (SMTP) |
| **Version Control** | Git, GitHub |
| **OS** | Linux (Ubuntu 20.04+ recommended) |

---

## 📁 Project Structure

```
Employee-Learning-Management-System/
│
├── 📄 manage.py                          # Django management script
├── 📄 requirements.txt                   # Python dependencies
├── 📄 README.md                          # This file
├── 📄 db.sqlite3                         # Development database
├── 📄 backup-db.py                       # Database backup script
│
├── 🗂️ config/                            # Django project settings
│   ├── __init__.py
│   ├── settings.py                       # Main settings
│   ├── urls.py                           # URL routing
│   ├── asgi.py                           # ASGI configuration
│   └── wsgi.py                           # WSGI configuration
│
├── 🗂️ accounts/                          # User management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│
├── 🗂️ course/                            # Course management app
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│
├── 🗂️ courseallocations/                 # Course allocation app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│
├── 🗂️ core/                              # Core utilities
│   ├── views.py
│   ├── urls.py
│   ├── models.py
│   └── templates/
│
├── 🗂️ notifications/                     # Notifications app
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 🗂️ emailsettings/                     # Email configuration
│   ├── models.py
│   ├── views.py
│   └── forms.py
│
├── 🗂️ feedback/                          # Feedback management
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 🗂️ quiz/                              # Quiz management
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 🗂️ results/                           # Result tracking
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 🗂️ search/                            # Search functionality
│   ├── views.py
│   └── urls.py
│
├── 🗂️ android/                           # Android app management
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── 🗂️ templates/                         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── ...
│
├── 🗂️ static/                            # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│
├── 🗂️ media/                             # User uploads
│   ├── documents/
│   ├── apk/
│   └── images/
│
└── 🗂️ locale/                            # Internationalization
    └── ...
```

---

## 🚀 Quick Start

### ⚡ 5-Minute Setup

```bash
# 1️⃣ Clone the repository
git clone https://github.com/vishnuvm1122/Employee-Learning-Management-System.git
cd Employee-Learning-Management-System

# 2️⃣ Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run migrations
python manage.py migrate

# 5️⃣ Create superuser
python manage.py createsuperuser

# 6️⃣ Start development server
python manage.py runserver

# 7️⃣ Access application
# Open: http://127.0.0.1:8000/
# Admin: http://127.0.0.1:8000/admin/
```

---

## 📖 Detailed Installation

### Prerequisites

Before installation, ensure you have:

- ✅ Ubuntu 20.04+ or Linux system (Windows with WSL supported)
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ MySQL 8.0 or higher
- ✅ Git
- ✅ 500MB disk space minimum

### Step 1️⃣: Verify System Requirements

```bash
# Check Python version
python3 --version
# Expected output: Python 3.8+

# Check pip
pip3 --version

# Check MySQL
mysql --version
# Expected output: mysql Ver 8.0+
```

**📦 Install Python (if needed):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev -y
```

**📦 Install MySQL (if needed):**
```bash
sudo apt update
sudo apt install mysql-server mysql-client libmysqlclient-dev -y
```

### Step 2️⃣: Clone Repository

```bash
# Clone the repository
git clone https://github.com/vishnuvm1122/Employee-Learning-Management-System.git

# Navigate to project
cd Employee-Learning-Management-System

# Verify you're in the right directory
ls -la
# You should see: manage.py, requirements.txt, config/, etc.
```

### Step 3️⃣: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# You should see (venv) in your terminal prompt
# Example: (venv) user@computer:~/Employee-Learning-Management-System$

# Verify activation
which python
# Should show: /path/to/venv/bin/python
```

### Step 4️⃣: Install Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install from requirements.txt
pip install -r requirements.txt

# Verify Django installation
python -m django --version
# Expected output: 4.0+

# Verify other key packages
pip list | grep -E "Django|mysqlclient|Django-MySQL"
```

**📋 Expected Packages:**
```
Django>=4.0
mysqlclient>=2.1.0
pillow>=9.0.0
requests>=2.27.0
python-decouple>=3.6
```

### Step 5️⃣: MySQL Database Setup

```bash
# Start MySQL service
sudo systemctl start mysql
sudo systemctl enable mysql

# Verify MySQL is running
sudo systemctl status mysql

# Connect to MySQL
sudo mysql -u root

# In MySQL console, run these commands:
```

**SQL Commands:**
```sql
-- Create database
CREATE DATABASE lmsmgmt 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Create dedicated database user
CREATE USER 'lmsuser'@'localhost' 
IDENTIFIED BY 'strong_password_here_123';

-- Grant all permissions
GRANT ALL PRIVILEGES ON lmsmgmt.* 
TO 'lmsuser'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SHOW GRANTS FOR 'lmsuser'@'localhost';

-- Exit
EXIT;
```

**⚠️ Important:** Replace `strong_password_here_123` with a strong password!

### Step 6️⃣: Configure Django Settings

```bash
# Navigate to settings file
nano config/settings.py
```

**Add/Update Database Configuration:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lmsmgmt',
        'USER': 'lmsuser',
        'PASSWORD': 'strong_password_here_123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
```

**Configure Email (Optional):**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

**Configure Allowed Hosts:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']
```

### Step 7️⃣: Environment Variables (Recommended)

```bash
# Create .env file
touch .env

# Edit it
nano .env
```

**Add to .env:**
```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=lmsmgmt
DATABASE_USER=lmsuser
DATABASE_PASSWORD=strong_password_here_123
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

**Update settings.py to use environment variables:**
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}
```

**Add to .gitignore:**
```
.env
*.pyc
__pycache__/
venv/
.venv/
*.sqlite3
db.sqlite3
media/
staticfiles/
.DS_Store
*.log
.idea/
.vscode/
```

### Step 8️⃣: Run Migrations

```bash
# Check project
python manage.py check

# Create new migrations (if models changed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, core, course, ...
Running migrations:
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_user_add_last_login_and_created... OK
  ...
```

### Step 9️⃣: Create Admin User

```bash
# Create superuser (administrator)
python manage.py createsuperuser

# You'll be prompted for:
# Username: admin
# Email: admin@example.com
# Password: (enter secure password)
# Password (again): (confirm)

# Superuser created successfully.
```

**💡 Use a strong password:** Mix uppercase, lowercase, numbers, and symbols.

### Step 🔟: Collect Static Files

```bash
# Create staticfiles directory
mkdir -p staticfiles

# Collect static files (for production)
python manage.py collectstatic --noinput

# Verify
ls -la staticfiles/
```

### Step 1️⃣1️⃣: Run Development Server

```bash
# Start the server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CONTROL-C.
```

**🌐 Access the Application:**
- **Main App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Login with:** Username/Email and password you just created

### Step 1️⃣2️⃣: Access on Local Network (Optional)

```bash
# Allow other devices to connect
python manage.py runserver 0.0.0.0:8000

# Find your IP address
hostname -I

# Other devices can access at: http://YOUR-IP:8000/
```

---

## ⚙️ Configuration

### Email Configuration

**Gmail Setup Example:**
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in .env

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
```

**Microsoft Exchange:**
```
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@company.com
EMAIL_HOST_PASSWORD=your-password
```

### Security Settings

**Production Checklist:**
```python
# settings.py

# Security
DEBUG = False  # Never True in production
SECRET_KEY = 'your-secret-key'  # Use environment variable
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}
```

---

## 🧪 Testing

### Run System Check

```bash
python manage.py check
```

### Run Test Suite

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test accounts

# Run with verbose output
python manage.py test -v 2

# Run specific test
python manage.py test accounts.tests.UserModelTest
```

### Test Critical Paths

- [ ] User registration and login
- [ ] Course creation and allocation
- [ ] Progress tracking
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] Password reset workflow
- [ ] Security monitoring

---

## 📊 Database

### Create Backup

```bash
# Backup database
mysqldump -u lmsuser -p lmsmgmt > lmsmgmt_backup.sql

# Or use Python script
python backup-db.py
```

### Restore Backup

```bash
# Restore database
mysql -u lmsuser -p lmsmgmt < lmsmgmt_backup.sql

# Verify
mysql -u lmsuser -p
> USE lmsmgmt;
> SHOW TABLES;
```

### Database Schema

```sql
-- Key tables
SHOW TABLES;

-- User table
DESC auth_user;

-- Course table
DESC course_course;

-- Progress tracking
DESC courseallocations_courseallocation;

-- Security logs
DESC accounts_loginattempt;
```

---

## 🔐 Security

### Authentication Methods

```python
# Django's built-in authentication
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

### Password Security

```python
# Use Django's password validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

### CSRF Protection

```html
<!-- Always include CSRF token in forms -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

### SQL Injection Prevention

```python
# ✅ SAFE - Using ORM
user = User.objects.get(username=username)

# ❌ UNSAFE - Raw SQL (Don't use!)
# User.objects.raw(f"SELECT * FROM auth_user WHERE username = '{username}'")
```

---

## 🩺 Troubleshooting

### Error: No module named 'django'

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import django; print(django.get_version())"
```

### Error: MySQL connection error

```bash
# Check MySQL is running
sudo systemctl status mysql

# Start if stopped
sudo systemctl start mysql

# Verify credentials
mysql -u lmsuser -p -h 127.0.0.1
# Password: (enter your password)

# Check in settings.py:
# - DATABASE_NAME matches
# - DATABASE_USER matches
# - DATABASE_PASSWORD matches
# - DATABASE_HOST is correct
# - DATABASE_PORT is correct (default 3306)
```

### Error: Static files not loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC settings in settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Verify directory
ls -la staticfiles/
```

### Error: Email not sending

```bash
# Test email configuration
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
1  # Should return 1 if successful

# Check settings:
# - EMAIL_HOST
# - EMAIL_PORT
# - EMAIL_HOST_USER
# - EMAIL_HOST_PASSWORD
# - EMAIL_USE_TLS
```

### Error: Permission denied

```bash
# Fix permissions
chmod +x manage.py
chmod 755 staticfiles/
chmod 755 media/

# Set correct owner
sudo chown -R $USER:$USER .
```

---

## 📝 Useful Commands

### Django Management Commands

```bash
# 🟢 Activate environment
source venv/bin/activate

# ▶️ Start development server
python manage.py runserver

# ▶️ Run on specific IP and port
python manage.py runserver 0.0.0.0:8000

# 🔍 Check project configuration
python manage.py check

# 🏗️ Create new migrations
python manage.py makemigrations

# 🗃️ Apply migrations
python manage.py migrate

# 📋 Show migration status
python manage.py showmigrations

# ↩️ Revert migrations
python manage.py migrate app_name 0001

# 👨‍💼 Create administrator
python manage.py createsuperuser

# 🎨 Collect static files
python manage.py collectstatic

# 🧪 Run tests
python manage.py test

# 🐚 Open Django shell
python manage.py shell

# 📊 Database shell
python manage.py dbshell

# 🔄 Run background tasks
python manage.py celery worker  # if Celery is installed
```

### Useful Bash Commands

```bash
# 🔵 Virtual Environment
source venv/bin/activate          # Activate
deactivate                        # Deactivate
python -m pip list               # List packages

# 📦 Pip
pip install -r requirements.txt   # Install all
pip install package_name         # Install specific
pip install --upgrade package    # Update
pip freeze > requirements.txt     # Update requirements

# 🗂️ Project Files
ls -la                            # List files
find . -name "*.pyc" -delete     # Remove Python cache
find . -name "__pycache__" -type d -exec rm -rf {} +

# 🔍 Search
grep -r "search_term" .          # Search in files
find . -name "*.py" -type f      # Find Python files

# 🛠️ Database
mysql -u lmsuser -p              # Connect to MySQL
mysqldump -u user -p db > backup.sql  # Backup DB
```

---

## 🎯 Project Objectives

✅ **Centralize** employee management and training  
✅ **Simplify** course allocation and tracking  
✅ **Automate** notifications and reminders  
✅ **Monitor** learning progress and completion  
✅ **Secure** employee and authentication data  
✅ **Integrate** mobile application support  
✅ **Improve** organizational training visibility  
✅ **Support** scalable learning platform  

---

## 🌟 Future Enhancements

- 🤖 AI-powered learning recommendations
- 💬 AI learning assistant/chatbot
- 📝 Online examinations module
- ❓ Advanced quiz management
- 📄 Assignment management system
- 🏆 Certificate generation
- 📊 Advanced analytics dashboard
- 🎮 Gamification features
- 📹 Live class support
- 🔔 Push notifications (iOS/Android)
- 🌍 Multi-language support
- 📱 Advanced mobile app
- 📈 Comprehensive reporting suite
- 🧩 LMS integrations (Blackboard, Canvas, etc.)

---

## 🩺 Production Deployment

### Using Gunicorn & Nginx

**Install Gunicorn:**
```bash
pip install gunicorn
```

**Create Gunicorn service:**
```bash
sudo nano /etc/systemd/system/lms.service
```

**Add:**
```ini
[Unit]
Description=LMS Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/Employee-Learning-Management-System
ExecStart=/path/to/venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable lms
sudo systemctl start lms
```

**Configure Nginx reverse proxy:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }
}
```

---

## 📄 License

[Add your license information here - MIT, GPL, Apache, etc.]

Example:
```
MIT License

Copyright (c) 2024 Vishnu VM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🔗 Links

- 🐙 **GitHub:** [vishnuvm1122/Employee-Learning-Management-System](https://github.com/vishnuvm1122/Employee-Learning-Management-System)
- 💼 **LinkedIn:** [vishnuvm1997](https://www.linkedin.com/in/vishnuvm1997/)
- 📧 **Email:** [vishnuedappal1122@gmail.com](mailto:vishnuedappal1122@gmail.com)
- 🌐 **Website:** [your-website.com]

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Support

For issues, questions, or suggestions:

- 📝 **Issues:** [GitHub Issues](https://github.com/vishnuvm1122/Employee-Learning-Management-System/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/vishnuvm1122/Employee-Learning-Management-System/discussions)
- 📧 **Email:** [vishnuedappal1122@gmail.com](mailto:vishnuedappal1122@gmail.com)

---

<div align="center">

**Built with ❤️ by Vishnu VM**

⭐ If this project helped you, please consider giving it a star!

</div>

---

**Last Updated:** September 1, 2024  
**Version:** 1.0.0  
**Status:** Active Development ✅
