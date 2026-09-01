# 🎓 Employee Learning Management System (LMS)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-Framework-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/Bootstrap-Frontend-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Linux-OS-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
  <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</p>

<p align="center">
  <strong>🚀 Secure • Scalable • Organized • Employee-Focused</strong>
</p>

<p align="center">
  A web-based Employee Learning Management System built with
  <strong>Python, Django, MySQL, HTML5, CSS3, JavaScript, and Bootstrap</strong>.
</p>

---

## 📌 Table of Contents

- [🌟 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🏗️ System Architecture](#️-system-architecture)
- [🛠️ Technology Stack](#️-technology-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Installation](#-installation)
- [🗄️ MySQL Setup](#️-mysql-setup)
- [⚙️ Django Configuration](#️-django-configuration)
- [📧 Email Configuration](#-email-configuration)
- [🔐 Authentication](#-authentication)
- [🛡️ Security Monitoring](#️-security-monitoring)
- [📚 Course Management](#-course-management)
- [🎯 Course Allocation](#-course-allocation)
- [📊 Learning Management](#-learning-management)
- [🔔 Notifications & Reminders](#-notifications--reminders)
- [📱 Android Application Support](#-android-application-support)
- [🧪 Testing](#-testing)
- [🔒 Production Security Checklist](#-production-security-checklist)
- [🚀 Production Architecture](#-production-architecture)
- [💾 Database Backup](#-database-backup)
- [🔄 Production Updates](#-production-updates)
- [🩺 Troubleshooting](#-troubleshooting)
- [📋 Useful Django Commands](#-useful-django-commands)
- [🎯 Project Objectives](#-project-objectives)
- [🌟 Future Enhancements](#-future-enhancements)
- [📈 Project Status](#-project-status)
- [👨‍💻 Development](#-development)
- [⚠️ Security Notice](#️-security-notice)
- [📄 License](#-license)
- [🔗 Project Links](#-project-links)

---

## 🌟 Overview

The **Employee Learning Management System (LMS)** is a centralized platform
designed to manage employee training, course allocation, learning activities,
notifications, email communication, and authentication-related monitoring.

The platform provides administrators with tools to manage employees, courses,
learning progress, system notifications, email services, security activity,
and Android application releases.

### 👨‍💼 Administration

Administrators can:

- 👤 Create and manage employee accounts
- 🔐 Manage authentication and access
- 📚 Create and manage training courses
- 🎯 Allocate courses to employees
- 📊 Monitor learning progress and completion
- 📧 Configure email services
- 🔔 Manage application notifications
- 📅 Configure daily and weekly reminders
- 🛡️ Monitor login and logout activity
- 💻 Track configured device and session information
- 🌐 Record configured login IP information
- 🚨 Detect configured suspicious login activity
- 🔑 Support password recovery
- 📱 Manage Android application versions
- 📦 Manage APK releases and downloads

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 👤 **User Management** | Create, edit, activate, deactivate, and manage employee accounts |
| 🔐 **Authentication** | Login, logout, session handling, and access control |
| 🔑 **Password Reset** | Forgot-password and password-reset workflow |
| 📚 **Course Management** | Create and manage employee training courses |
| 🎯 **Course Allocation** | Assign courses to employees |
| 📊 **Progress Tracking** | Monitor learning progress and completion |
| 📧 **Email Settings** | Configure SMTP and application email services |
| 🔔 **Notifications** | Application and email notifications |
| 📅 **Daily Reminders** | Automated daily learning reminders |
| 📆 **Weekly Reminders** | Automated weekly learning reminders |
| 🛡️ **Security Monitoring** | Monitor authentication-related activity |
| 💻 **Device Tracking** | Record configured device and browser information |
| 🌐 **IP Tracking** | Record configured login IP information |
| 🚨 **Suspicious Login Detection** | Detect configured potentially suspicious authentication activity |
| 📱 **Android Integration** | Application version and release management |
| 📦 **APK Management** | Manage APK files, releases, version information, and downloads |
| 👨‍💼 **Admin Dashboard** | Centralized administrative management |
| 🗄️ **MySQL Database** | Relational database storage |

---

## 🏗️ System Architecture

```text
                              🌐 USER
                                │
                                ▼
                     ┌─────────────────────┐
                     │    🌍 WEB BROWSER   │
                     │ HTML5 • CSS3 • JS   │
                     │     Bootstrap       │
                     └──────────┬──────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │     🐍 DJANGO       │
                     │      BACKEND        │
                     └──────────┬──────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
       👤 USER MANAGEMENT   📚 LMS           🛡️ SECURITY
              │                 │                 │
              ▼                 ▼                 ▼
       🔐 Authentication   📖 Courses       🔐 Login Monitoring
       👥 User Accounts    🎯 Allocation    💻 Device Tracking
       🔑 Permissions      📊 Progress      🌐 IP Tracking
                                              🚨 Suspicious Login
              │                 │                 │
              └─────────────────┼─────────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
          ┌───────────────┐           ┌────────────────┐
          │ 🗄️ MySQL      │           │ 📧 SMTP Server │
          │   Database    │           │    Email       │
          └───────────────┘           └────────────────┘
                  │                           │
                  ▼                           ▼
          Application Data             🔔 Notifications
          Learning Data                🔑 Password Reset
          Security Logs                📅 Reminders
🛠️ Technology Stack
🐍 Backend
Python 3.x
Django
Django ORM
Django Authentication
🎨 Frontend
HTML5
CSS3
JavaScript
Bootstrap
🗄️ Database
MySQL
📧 Email
SMTP
Django Email Backend
🐙 Version Control
Git
GitHub
🐧 Operating System
Ubuntu / Linux recommended
📁 Project Structure

ℹ️ Replace <django_project> and <django_app> with the actual names
used by your source repository.

Employee-Learning-Management-System/
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
├── .env.example
├── README.md
└── INSTALL.md
🚀 Installation
1️⃣ Clone the Repository
git clone https://github.com/vishnuvm1122/Employee-Learning-Management-System.git
cd Employee-Learning-Management-System
2️⃣ Check Python
python3 --version

Recommended:

Python 3.x

If Python is not installed:

sudo apt update
sudo apt install python3 python3-pip python3-venv -y
3️⃣ Create a Virtual Environment
python3 -m venv venv

Activate it:

source venv/bin/activate

You should see something similar to:

(venv) user@computer:~/Employee-Learning-Management-System$
4️⃣ Upgrade pip
python -m pip install --upgrade pip
5️⃣ Install Project Dependencies

If requirements.txt exists:

pip install -r requirements.txt

Verify Django:

python -m django --version
🗄️ MySQL Setup
6️⃣ Install MySQL

On Ubuntu:

sudo apt update
sudo apt install mysql-server mysql-client -y

Check MySQL:

sudo systemctl status mysql

Start MySQL if required:

sudo systemctl start mysql

Enable MySQL at boot:

sudo systemctl enable mysql
7️⃣ Create the Database

Open MySQL:

sudo mysql

Create the database:

CREATE DATABASE lmsmgmt
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

Create a dedicated database user:

CREATE USER 'lmsuser'@'localhost'
IDENTIFIED BY 'CHANGE_THIS_PASSWORD';

Grant permissions:

GRANT ALL PRIVILEGES ON lmsmgmt.* TO 'lmsuser'@'localhost';

Apply privileges:

FLUSH PRIVILEGES;

Exit:

EXIT;

⚠️ Replace CHANGE_THIS_PASSWORD with a strong, unique password.
Never publish real credentials in GitHub.

⚙️ Django Configuration
8️⃣ Configure the Database

Configure the database in settings.py, or preferably load the values
from environment variables.

Example:

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

🔐 For production, do not hard-code database passwords in source code.

9️⃣ Environment Variables

Create a local .env file if the project uses environment variables:

touch .env

Example:

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
🚫 Never commit .env

Recommended .gitignore entries:

.env
*.pyc
__pycache__/
venv/
.venv/
media/
staticfiles/
*.log
🗃️ Database Migration
🔟 Run Migrations

Create migrations when required:

python manage.py makemigrations

Apply migrations:

python manage.py migrate

Check migration status:

python manage.py showmigrations
👨‍💼 Create Administrator
1️⃣1️⃣ Create a Superuser
python manage.py createsuperuser

Enter:

Username
Email
Password

🔐 Use a strong administrator password.

🎨 Static & Media Files
1️⃣2️⃣ Collect Static Files

For production:

python manage.py collectstatic

Verify the following settings:

STATIC_URL
STATIC_ROOT
MEDIA_URL
MEDIA_ROOT
▶️ Run the Application
1️⃣3️⃣ Start Development Server
python manage.py runserver

Open:

http://127.0.0.1:8000/
🌐 Run on a Local Network

To allow another device on the local network to connect:

python manage.py runserver 0.0.0.0:8000

Then open:

http://SERVER-IP:8000/

⚠️ Django's development server is for development/testing and should not
be used as the production web server.

🔑 Admin Panel

Open:

http://127.0.0.1:8000/admin/

Log in using the Django superuser account.

📧 Email Configuration

The LMS can use SMTP for:

🔑 Password reset emails
🚨 Suspicious login alerts
📚 Course allocation notifications
🔔 User notifications
📅 Daily reminders
📆 Weekly reminders
📢 System notifications

Example:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-password"

DEFAULT_FROM_EMAIL = "your-email@example.com"

🔐 Store SMTP credentials in environment variables or a secure secret
management system in production.

🔐 Authentication
🔑 Password Reset Workflow
👤 User
   │
   ▼
🔑 Forgot Password
   │
   ▼
📧 Enter Email
   │
   ▼
🔐 Django Authentication
   │
   ▼
📨 Password Reset Email
   │
   ▼
🔗 Reset Link
   │
   ▼
🔑 Create New Password
   │
   ▼
✅ Login
🛡️ Security Monitoring

The LMS includes security-related functionality for monitoring
authentication activity.

Depending on the project configuration, tracked information may include:

🌐 IP address
💻 Device information
🌍 Browser information
🖥️ Operating system
🧾 User-Agent
🔐 Session information
🕐 Login time
🕐 Logout time

Configured security conditions can be used to identify potentially
suspicious login activity.

🔒 Security and employee data collection should follow applicable
organizational policies, privacy requirements, and access-control rules.

🚨 Suspicious Login Notification

Typical workflow:

🔐 Login
   │
   ▼
📋 Capture Login Information
   │
   ▼
🛡️ Security Check
   │
   ├──────────────────┐
   │                  │
   ▼                  ▼
✅ Normal          🚨 Suspicious
   │                  │
   ▼                  ▼
Continue          Log Activity
                      │
                      ▼
                  📧 Email Alert
📚 Course Management

Administrators can manage employee training courses.

Typical workflow:

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
🏆 Completion
🎯 Course Allocation

Course allocation connects employees with their assigned training.

👤 Employee + 📚 Course
          │
          ▼
   🎯 Course Allocation
          │
          ▼
   👨‍💻 Employee Dashboard
          │
          ▼
     📖 Assigned Course
          │
          ▼
        📊 Learning
📊 Learning Management

Employees can access assigned learning content and track their learning
activities.

Possible learning information includes:

📚 Assigned courses
▶️ Learning content
📈 Progress
⏳ Pending activities
✅ Completed activities
🏆 Course completion
🔔 Notifications & Reminders

The system can provide notifications for important events.

Examples:

📚 Course allocation
📧 Email notifications
🔑 Password reset
🚨 Suspicious login alerts
📅 Daily reminders
📆 Weekly reminders
⚙️ System notifications
📅 Daily Reminder
👤 Employee
     │
     ▼
📖 Pending Learning Activity
     │
     ▼
📧 Daily Reminder
📆 Weekly Reminder
👤 Employee
     │
     ▼
📊 Learning Status
     │
     ▼
📧 Weekly Reminder

ℹ️ Scheduler configuration should be verified against the actual project
implementation before production deployment.

📱 Android Application Support

Where Android integration is enabled, the backend can support application
version management.

Possible version information includes:

🏷️ Version name
🔢 Version code
📦 APK file
📏 APK size
📝 Release notes
🟢 Active version
🔄 Force update
📥 Download count
📱 Android Version Workflow
📱 Android App
      │
      ▼
🔢 Installed Version
      │
      ▼
🐍 Django Backend
      │
      ▼
🔍 Version Comparison
      │
   ┌──┴──────┐
   │         │
   ▼         ▼
🟢 Latest   🔄 Update
   │         │
   ▼         ▼
Continue   📦 Download Update
🧪 Testing

Run Django's system check:

python manage.py check

Run the test suite:

python manage.py test
👤 User Management
 Create employee
 Edit employee
 Activate/deactivate employee
 Verify permissions
🔐 Authentication
 Login
 Logout
 Invalid login
 Password reset
 Session handling
📚 LMS
 Create course
 Edit course
 Allocate course
 Access assigned course
 Verify progress
📧 Email
 Password reset email
 Course notification
 Suspicious login email
 Daily reminder
 Weekly reminder
🛡️ Security
 Login activity
 Logout activity
 Device information
 IP information
 Suspicious login detection
🔒 Production Security Checklist

Before deploying to production:

 DEBUG=False
 SECRET_KEY protected
 Database password protected
 SMTP password protected
 .env excluded from GitHub
 HTTPS enabled
 ALLOWED_HOSTS configured
 CSRF configuration reviewed
 Secure cookies enabled
 Static files configured
 Media files configured
 Database backup configured
 Administrator password secured
 Dependencies reviewed and updated
 Application tested
 Email functionality tested
 Login monitoring tested
 Error logging configured
 Server firewall configured
 Production web server configured
 Database access restricted
 Backup restoration tested
🔐 Security Best Practices
🚫 Never commit passwords.
🚫 Never commit .env files.
🔑 Never expose the Django SECRET_KEY.
🔒 Use HTTPS in production.
🛡️ Use strong administrator passwords.
🔄 Keep dependencies updated.
💾 Configure regular database backups.
👨‍💼 Restrict administrative access.
📋 Review application logs regularly.
🔐 Protect employee and authentication data.
🌐 Configure ALLOWED_HOSTS correctly.
🍪 Enable secure cookie settings in production.
🧪 Test security controls before deployment.
📜 Follow organizational privacy and security requirements.
🚀 Production Architecture
                         🌐 INTERNET
                              │
                              ▼
                         🔒 HTTPS
                              │
                              ▼
                  ┌────────────────────┐
                  │   Nginx / Apache   │
                  │ Reverse Proxy      │
                  └─────────┬──────────┘
                            │
                            ▼
                  ┌────────────────────┐
                  │ Django / WSGI      │
                  │ Application        │
                  └─────────┬──────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
        🗄️ MySQL        📧 SMTP       📱 Android
         Database        Server          Client
              │
              ▼
       💾 Application Data
       📚 Learning Data
       🛡️ Security Logs
💾 Database Backup

Create a MySQL backup:

mysqldump -u lmsuser -p lmsmgmt > lmsmgmt_backup.sql

Restore the backup:

mysql -u lmsuser -p lmsmgmt < lmsmgmt_backup.sql

💡 Store database backups securely and periodically test the restoration
process.

🔄 Production Updates

Activate the virtual environment:

source venv/bin/activate

Install/update dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Collect static files:

python manage.py collectstatic

Restart the production application/service according to your deployment
configuration.

⚠️ Always test migrations and application changes before applying them to
a production system.

🩺 Troubleshooting
❌ No module named django
source venv/bin/activate
pip install -r requirements.txt
🐬 MySQL Connection Error

Check MySQL:

sudo systemctl status mysql

Verify:

Database name
Database username
Database password
Database host
Database port
MySQL service status
🗃️ Missing Database Tables

Run:

python manage.py makemigrations
python manage.py migrate
🎨 Static Files Not Loading

Run:

python manage.py collectstatic

Then verify:

STATIC_URL
STATIC_ROOT
MEDIA_URL
MEDIA_ROOT
📧 Email Not Sending

Verify:

SMTP host
SMTP port
SMTP username
SMTP password
TLS/SSL configuration
Firewall rules
SMTP provider configuration
Sender address configuration

Also check:

📬 Spam/junk folder
📝 Django logs
🖥️ Application logs
🔥 Firewall configuration
📋 Useful Django Commands
Purpose	Command
🟢 Activate environment	source venv/bin/activate
▶️ Start server	python manage.py runserver
🔍 Check project	python manage.py check
🏗️ Create migrations	python manage.py makemigrations
🗃️ Apply migrations	python manage.py migrate
📋 Show migrations	python manage.py showmigrations
👨‍💼 Create admin	python manage.py createsuperuser
🎨 Collect static	python manage.py collectstatic
🧪 Run tests	python manage.py test
🐚 Open shell	python manage.py shell
🎯 Project Objectives

The main objectives of this LMS are:

👤 Centralize employee management
🔐 Provide secure authentication
📚 Manage employee training courses
🎯 Simplify course allocation
📊 Monitor learning progress
📧 Automate email communication
🔔 Provide notifications and reminders
🚨 Monitor configured suspicious authentication activity
💻 Track configured login and device activity
📱 Support mobile application integration
📈 Improve employee training visibility
🛡️ Improve application security
🌟 Future Enhancements

Potential future improvements include:

🤖 AI-powered learning recommendations
💬 AI learning assistant
🧠 AI chatbot
📝 Online examinations
❓ Quiz management
📄 Assignment management
🏆 Certificate generation
📊 Advanced analytics
🎮 Gamification
📹 Live classes
🔔 Push notifications
🌍 Multi-language support
📱 Advanced mobile application
📈 Advanced management reports
🤖 Automated learning recommendations
📊 Learning analytics dashboard
🧩 Additional LMS integrations
📈 Project Status

🚧 Status: Active Development

The platform is designed as an extensible Employee Learning Management System
combining:

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
👨‍💻 Development

The project is designed to be maintained using:

🐍 Python
🌐 Django
🐬 MySQL
🎨 HTML5 / CSS3
⚡ JavaScript
🧩 Bootstrap
🐙 Git / GitHub
🐧 Linux
⚠️ Security Notice

This project handles authentication, employee information, email
configuration, and security-related activity.

For production deployments:

🔐 Never commit passwords.
🚫 Never commit .env files.
🔑 Never expose the Django SECRET_KEY.
🔒 Use HTTPS.
🛡️ Use strong administrator passwords.
🔄 Keep dependencies updated.
💾 Configure database backups.
👨‍💼 Restrict administrative access.
📋 Review application logs regularly.
🔐 Protect employee and authentication information.
📜 Follow applicable organizational security and privacy requirements.

⚠️ Only perform security testing against systems, applications, and
accounts that you own or have explicit authorization to test.

📄 License

Add the organization's actual license information here.

Example:

MIT License

ℹ️ Replace the example above with the license that actually applies to
this project.

🔗 Project Links
🐙 GitHub Repository

https://github.com/vishnuvm1122/Employee-Learning-Management-System.git

💼 LinkedIn

https://www.linkedin.com/in/vishnuvm1997/

<p align="center"> <strong>🎓 Employee Learning Management System</strong> <br><br> 🔐 Secure • 📚 Organized • 🚀 Scalable • 👨‍💼 Employee-Focused <br><br> Built with 🐍 <strong>Python</strong> & 🌐 <strong>Django</strong> </p> '''
