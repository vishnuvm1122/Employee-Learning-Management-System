# 🎓 Employee Learning Management System (LMS)

<p align="center">

### 🚀 Secure • Scalable • Employee-Focused Learning Platform

A complete web-based Learning Management System built with **Python, Django, MySQL, HTML, CSS, JavaScript and Bootstrap** for managing employees, courses, course allocations, learning activities, notifications, email communication and security monitoring.

</p>

---

## 📌 Project Overview

The **Employee Learning Management System (LMS)** is a centralized platform designed to manage employee training and learning activities.

It provides administrators with tools to:

* 👤 Create and manage employees
* 🔐 Manage authentication and access
* 📚 Create and manage courses
* 🎯 Allocate courses to employees
* 📊 Monitor learning progress
* 📧 Configure email services
* 🔔 Send notifications and reminders
* 🛡️ Monitor login and logout activity
* 💻 Track device/session information
* 🚨 Detect suspicious login activity
* 🔑 Provide password recovery
* 📱 Support Android application integration
* 📈 Monitor and manage learning activities

---

# ✨ Key Features

| Feature                 | Description                                    |
| ----------------------- | ---------------------------------------------- |
| 👤 User Management      | Create, edit and manage employee accounts      |
| 🔐 Authentication       | Secure login and logout functionality          |
| 🔑 Password Reset       | Forgot-password and password-reset workflow    |
| 📚 Course Management    | Create and manage training courses             |
| 🎯 Course Allocation    | Assign courses to employees                    |
| 📊 Progress Tracking    | Monitor employee learning progress             |
| 📧 Email Settings       | Configure SMTP/email services                  |
| 🔔 Notifications        | Application and email notifications            |
| 📅 Daily Reminders      | Automated daily learning reminders             |
| 📆 Weekly Reminders     | Automated weekly learning reminders            |
| 🛡️ Security Monitoring | Monitor authentication activity                |
| 💻 Device Tracking      | Record device/browser information              |
| 🌐 IP Tracking          | Record login IP information                    |
| 🚨 Suspicious Login     | Detect configured suspicious activity          |
| 📱 Android Integration  | Support Android application/version management |
| 📦 APK Management       | Manage application versions and APK downloads  |
| 👨‍💼 Admin Dashboard   | Centralized administration                     |
| 🗄️ MySQL               | Relational database support                    |

---

# 🏗️ System Architecture

```text
                         🌐 USER
                           │
                           ▼
                  ┌───────────────────┐
                  │   Web Browser     │
                  │ HTML/CSS/JS       │
                  │ Bootstrap         │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │      Django       │
                  │     Backend       │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼──────────────────┐
          │                 │                  │
          ▼                 ▼                  ▼
    👤 User Management   📚 LMS             🛡️ Security
          │                 │                  │
          ▼                 ▼                  ▼
    Authentication    Course Management   Login Monitoring
    User Creation     Course Allocation   Device Tracking
    Permissions        Progress            Suspicious Login
          │                 │                  │
          └─────────────────┼──────────────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       🗄️ MySQL Database              📧 SMTP
                                      Email Server
             │                             │
             ▼                             ▼
       Application Data            Notifications
       Learning Data              Password Reset
       Security Logs              Reminders
```

---

# 🛠️ Technology Stack

## Backend

* 🐍 **Python**
* 🌐 **Django**
* 🗄️ **Django ORM**
* 🔐 **Django Authentication**

## Frontend

* 🌐 **HTML5**
* 🎨 **CSS3**
* ⚡ **JavaScript**
* 🧩 **Bootstrap**

## Database

* 🐬 **MySQL**

## Email

* 📧 SMTP
* Django Email Backend

## Version Control

* 🐙 Git
* 🐙 GitHub

## Operating System

* 🐧 Ubuntu / Linux recommended

---

# 📁 Project Structure

> **Note:** The exact application directory names should match the source
> repository. The structure below describes the Django organization used by
> the project.

```text
lmsmgmt/
│
├── manage.py
│
├── <django_project>/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── <django_app>/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   │
│   ├── migrations/
│   │   └── ...
│   │
│   └── templates/
│       └── ...
│
├── templates/
│   ├── base.html
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
│
├── requirements.txt
├── .gitignore
├── .env
├── README.md
└── INSTALL.md
```

---

# 📦 Installation

## 1️⃣ Clone the Repository

Open a terminal and run:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project:

```bash
cd lmsmgmt
```

---

## 2️⃣ Check Python

Check the installed Python version:

```bash
python3 --version
```

Recommended:

```text
Python 3.x
```

If Python is not installed:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

---

# 3️⃣ Create Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

You should see something similar to:

```text
(venv) user@computer:~/lmsmgmt$
```

---

# 4️⃣ Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

# 5️⃣ Install Project Dependencies

If the repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

Verify Django:

```bash
python -m django --version
```

---

# 🐬 6️⃣ Install MySQL

On Ubuntu:

```bash
sudo apt update
sudo apt install mysql-server mysql-client -y
```

Check MySQL:

```bash
sudo systemctl status mysql
```

Start MySQL if necessary:

```bash
sudo systemctl start mysql
```

Enable MySQL at boot:

```bash
sudo systemctl enable mysql
```

---

# 🗄️ 7️⃣ Create Database

Open MySQL:

```bash
sudo mysql
```

Create the database:

```sql
CREATE DATABASE lmsmgmt
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Create a database user:

```sql
CREATE USER 'lmsuser'@'localhost'
IDENTIFIED BY 'CHANGE_THIS_PASSWORD';
```

Grant permissions:

```sql
GRANT ALL PRIVILEGES ON lmsmgmt.* TO 'lmsuser'@'localhost';
```

Apply privileges:

```sql
FLUSH PRIVILEGES;
```

Exit:

```sql
EXIT;
```

⚠️ **Security:** Replace `CHANGE_THIS_PASSWORD` with a strong password.

---

# ⚙️ 8️⃣ Configure Django Database

Open your Django settings:

```text
settings.py
```

Example configuration:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "lmsmgmt",
        "USER": "lmsuser",
        "PASSWORD": "CHANGE_THIS_PASSWORD",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

For production, use environment variables instead of storing passwords directly
inside `settings.py`.

---

# 🔐 9️⃣ Environment Configuration

Create a `.env` file if the project is configured to use environment variables:

```bash
touch .env
```

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=False

DATABASE_NAME=lmsmgmt
DATABASE_USER=lmsuser
DATABASE_PASSWORD=your-database-password
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=your-email@example.com
```

🚨 **Never upload `.env` to a public GitHub repository.**

Add it to `.gitignore`:

```gitignore
.env
```

---

# 🗃️ 🔟 Run Django Migrations

Create migrations if required:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Check migration status:

```bash
python manage.py showmigrations
```

---

# 👨‍💼 1️⃣1️⃣ Create Administrator

Create a Django administrator:

```bash
python manage.py createsuperuser
```

Enter:

```text
Username
Email
Password
```

Use a strong password.

---

# 🎨 1️⃣2️⃣ Collect Static Files

For production:

```bash
python manage.py collectstatic
```

Make sure the following are correctly configured:

```text
STATIC_URL
STATIC_ROOT
MEDIA_URL
MEDIA_ROOT
```

---

# ▶️ 1️⃣3️⃣ Start Development Server

Run:

```bash
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

---

# 🌐 1️⃣4️⃣ Run on Local Network

To make the development server accessible from another device:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then access:

```text
http://SERVER-IP:8000/
```

⚠️ Do not use Django's development server as the production web server.

---

# 🔑 1️⃣5️⃣ Admin Panel

Open:

```text
/admin/
```

Example:

```text
http://127.0.0.1:8000/admin/
```

Log in using the superuser account.

---

# 📧 Email Configuration

The LMS can use SMTP for:

* 🔑 Password reset emails
* 🚨 Suspicious login alerts
* 📚 Course allocation notifications
* 🔔 User notifications
* 📅 Daily reminders
* 📆 Weekly reminders
* 📢 System notifications

Example:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-password"

DEFAULT_FROM_EMAIL = "your-email@example.com"
```

For production, store credentials securely in environment variables.

---

# 🔑 Password Reset Workflow

```text
👤 User
   │
   ▼
Forgot Password
   │
   ▼
Enter Email
   │
   ▼
Django Authentication
   │
   ▼
📧 Password Reset Email
   │
   ▼
Reset Link
   │
   ▼
Create New Password
   │
   ▼
🔐 Login
```

---

# 🛡️ Security Monitoring

The LMS includes security-related functionality for monitoring authentication
activity.

Potentially tracked information includes:

```text
IP Address
Device
Browser
Operating System
User-Agent
Session
Login Time
Logout Time
```

The system can use configured conditions to identify potentially suspicious
login activity.

---

# 🚨 Suspicious Login Notification

Typical workflow:

```text
🔐 Login
   │
   ▼
Capture Login Information
   │
   ▼
Security Check
   │
   ├───────────────┐
   │               │
   ▼               ▼
Normal          Suspicious
   │               │
   ▼               ▼
Continue       Log Activity
                   │
                   ▼
             📧 Email Alert
```

---

# 📚 Course Management

Administrators can manage employee training courses.

Typical workflow:

```text
👨‍💼 Administrator
        │
        ▼
📚 Create Course
        │
        ▼
📝 Add Course Information
        │
        ▼
💾 Save Course
        │
        ▼
🎯 Allocate Course
        │
        ▼
👤 Employee
        │
        ▼
📖 Learning
        │
        ▼
📊 Progress
        │
        ▼
✅ Completion
```

---

# 🎯 Course Allocation

Course allocation connects employees with their assigned training.

```text
Employee
   +
Course
   │
   ▼
Course Allocation
   │
   ▼
Employee Dashboard
   │
   ▼
Assigned Course
   │
   ▼
Learning
```

---

# 📊 Learning Management

Employees can access assigned learning content and track their learning
activities.

Possible learning information includes:

* 📚 Assigned courses
* ▶️ Learning content
* 📈 Progress
* ⏳ Pending activities
* ✅ Completed activities
* 🏆 Course completion

---

# 🔔 Notifications

The system can provide notifications for important events.

Examples:

```text
📚 Course Allocation
📧 Email Notification
🔑 Password Reset
🚨 Suspicious Login
📅 Daily Reminder
📆 Weekly Reminder
⚙️ System Notification
```

---

# 📅 Automated Reminders

The LMS can provide scheduled reminders.

### Daily

```text
Employee
   ↓
Pending Learning Activity
   ↓
📧 Daily Reminder
```

### Weekly

```text
Employee
   ↓
Learning Status
   ↓
📧 Weekly Reminder
```

The scheduler configuration should be checked according to the actual project
implementation before production deployment.

---

# 📱 Android Application Support

Where Android integration is enabled, the backend can support application
version management.

Possible version information:

```text
Version Name
Version Code
APK File
APK Size
Release Notes
Active Version
Force Update
Download Count
```

Version workflow:

```text
📱 Android App
      │
      ▼
Installed Version
      │
      ▼
Django Backend
      │
      ▼
Version Comparison
      │
   ┌──┴──┐
   │     │
Latest  Update
   │     │
   ▼     ▼
Continue 📦 Update
```

---

# 🧪 Testing

Run Django's system check:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

Test the following before production:

### 👤 User Management

* [ ] Create employee
* [ ] Edit employee
* [ ] Activate/deactivate employee
* [ ] Verify permissions

### 🔐 Authentication

* [ ] Login
* [ ] Logout
* [ ] Invalid login
* [ ] Password reset
* [ ] Session handling

### 📚 LMS

* [ ] Create course
* [ ] Edit course
* [ ] Allocate course
* [ ] Access assigned course
* [ ] Verify progress

### 📧 Email

* [ ] Password reset email
* [ ] Course notification
* [ ] Suspicious login email
* [ ] Daily reminder
* [ ] Weekly reminder

### 🛡️ Security

* [ ] Login activity
* [ ] Logout activity
* [ ] Device information
* [ ] IP information
* [ ] Suspicious login detection

---

# 🐙 GitHub Setup

Initialize Git:

```bash
git init
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Initial LMS implementation"
```

Set main branch:

```bash
git branch -M main
```

Add GitHub repository:

```bash
git remote add origin <YOUR-GITHUB-REPOSITORY-URL>
```

Push:

```bash
git push -u origin main
```

---

# 🚫 Recommended `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual Environment
venv/
.venv/
env/

# Environment
.env

# Django
db.sqlite3
staticfiles/

# User uploads
media/

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Logs
*.log

# Secrets
*.pem
*.key
```

---

# 🔒 Production Security Checklist

Before deploying:

```text
[ ] DEBUG=False
[ ] SECRET_KEY protected
[ ] Database password protected
[ ] SMTP password protected
[ ] .env excluded from GitHub
[ ] HTTPS enabled
[ ] ALLOWED_HOSTS configured
[ ] CSRF configuration reviewed
[ ] Secure cookies enabled
[ ] Static files configured
[ ] Media files configured
[ ] Database backup configured
[ ] Administrator password secured
[ ] Dependencies updated
[ ] Application tested
[ ] Email functionality tested
[ ] Login monitoring tested
```

---

# 🚀 Production Architecture

```text
                    🌐 INTERNET
                         │
                         ▼
                    🔒 HTTPS
                         │
                         ▼
                 ┌───────────────┐
                 │ Nginx / Apache│
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Django / WSGI │
                 └───────┬───────┘
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
          🗄️ MySQL     📧 SMTP     📱 Android
          Database     Server       Client
```

---

# 💾 Database Backup

Create a MySQL backup:

```bash
mysqldump -u lmsuser -p lmsmgmt > lmsmgmt_backup.sql
```

Restore:

```bash
mysql -u lmsuser -p lmsmgmt < lmsmgmt_backup.sql
```

Store backups securely.

---

# 🔄 Updating the Application

Pull the latest code:

```bash
git pull origin main
```

Activate the environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Collect static files:

```bash
python manage.py collectstatic
```

Restart the production application if required.

---

# 🩺 Troubleshooting

## `No module named django`

```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## MySQL Connection Error

Check:

```bash
sudo systemctl status mysql
```

Verify:

```text
Database name
Database username
Database password
Database host
Database port
```

---

## Missing Database Tables

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Static Files Not Loading

Run:

```bash
python manage.py collectstatic
```

Then check:

```text
STATIC_URL
STATIC_ROOT
```

---

## Email Not Sending

Verify:

```text
SMTP Host
SMTP Port
SMTP Username
SMTP Password
TLS / SSL
Firewall
SMTP Provider
```

Also check the spam/junk folder.

---

# 📋 Useful Django Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python manage.py runserver

# Check project
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Create admin
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

---

# 🎯 Project Objectives

The main objectives of this LMS are:

1. 👤 Centralize employee management
2. 🔐 Provide secure authentication
3. 📚 Manage employee training courses
4. 🎯 Simplify course allocation
5. 📊 Monitor learning progress
6. 📧 Automate email communication
7. 🔔 Provide notifications and reminders
8. 🚨 Monitor suspicious authentication activity
9. 💻 Track login/device activity
10. 📱 Support mobile application integration
11. 📈 Improve employee training visibility
12. 🛡️ Improve application security

---

# 🌟 Future Enhancements

Potential future improvements include:

* 🤖 AI-powered learning recommendations
* 💬 AI learning assistant
* 🧠 AI chatbot
* 📝 Online examinations
* ❓ Quiz management
* 📄 Assignment management
* 🏆 Certificate generation
* 📊 Advanced analytics
* 🎮 Gamification
* 📹 Live classes
* 🔔 Push notifications
* 🌍 Multi-language support
* 📱 Advanced mobile application
* 📈 Advanced management reports
* 🤖 Automated learning recommendations

---

# 📌 Project Status

**Status:** 🚧 Active Development

The platform is designed as an extensible Employee Learning Management
System combining:

```text
👤 User Management
        +
🔐 Authentication
        +
📚 Course Management
        +
🎯 Course Allocation
        +
📊 Learning Progress
        +
📧 Email Management
        +
🔔 Notifications
        +
🛡️ Security Monitoring
        +
📱 Mobile Integration
        =
🎓 Employee Learning Management System
```

---

# 👨‍💻 Development

The project is designed to be maintained using:

```text
🐍 Python
🌐 Django
🐬 MySQL
🎨 HTML / CSS
⚡ JavaScript
🧩 Bootstrap
🐙 Git / GitHub
🐧 Linux
```

---

# ⚠️ Security Notice

This project handles authentication, employee information, email
configuration and security-related activity.

For production deployments:

* Never commit passwords.
* Never commit `.env` files.
* Never expose Django `SECRET_KEY`.
* Use HTTPS.
* Use strong administrator passwords.
* Keep dependencies updated.
* Configure database backups.
* Restrict administrative access.
* Review application logs regularly.

Only perform security testing against systems and accounts that you own or
have explicit authorization to test.

---

# 📄 License

Add the organization's license information here.

Example:

```text
Copyright © Hailstone Innovations Pvt Ltd.

All rights reserved unless otherwise specified.
```

---

# 📞 Support

For project-related support, configuration, deployment, or development
questions, contact the project administrator/development team.

---

<p align="center">

### 🎓 Employee Learning Management System

**Secure • Organized • Scalable • Employee-Focused**

🚀 **Built with Python & Django**

</p>
