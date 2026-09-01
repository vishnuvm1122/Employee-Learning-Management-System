ete web-based Learning Management System built with Python, Django,
MySQL, HTML, CSS, JavaScript, and Bootstrap for managing employees, courses,
course allocations, learning activities, notifications, email communication,
and security monitoring.


1. PROJECT OVERVIEW
===================

The Employee Learning Management System (LMS) is a centralized platform
designed to manage employee training and learning activities.

It provides administrators with tools to:

- Create and manage employees
- Manage authentication and access
- Create and manage courses
- Allocate courses to employees
- Monitor learning progress
- Configure email services
- Send notifications and reminders
- Monitor login and logout activity
- Track device and session information
- Detect configured suspicious login activity
- Provide password recovery
- Support Android application integration
- Manage Android application versions and APK downloads
- Monitor learning activities


2. KEY FEATURES
===============

User Management
    Create, edit, activate, and manage employee accounts.

Authentication
    Secure login and logout functionality.

Password Reset
    Forgot-password and password-reset workflow.

Course Management
    Create and manage employee training courses.

Course Allocation
    Assign courses to employees.

Progress Tracking
    Monitor employee learning progress and completion.

Email Settings
    Configure SMTP and email services.

Notifications
    Application and email notifications.

Daily Reminders
    Automated daily learning reminders.

Weekly Reminders
    Automated weekly learning reminders.

Security Monitoring
    Monitor authentication and account activity.

Device Tracking
    Record configured device and browser information.

IP Tracking
    Record login IP information.

Suspicious Login Detection
    Detect configured suspicious authentication activity.

Android Integration
    Support Android application and version management.

APK Management
    Manage application versions, APK files, release notes, and downloads.

Admin Dashboard
    Centralized administration.

MySQL
    Relational database support.


3. SYSTEM ARCHITECTURE
======================

                         USER
                           |
                           v
                  +-------------------+
                  |    Web Browser    |
                  | HTML/CSS/JS       |
                  | Bootstrap         |
                  +---------+---------+
                            |
                            v
                  +-------------------+
                  |      Django       |
                  |     Backend       |
                  +---------+---------+
                            |
          +-----------------+-----------------+
          |                 |                 |
          v                 v                 v
   User Management         LMS           Security
          |                 |                 |
          v                 v                 v
   Authentication    Course Management   Login Monitoring
   User Creation     Course Allocation   Device Tracking
   Permissions       Progress Tracking   Suspicious Login
          |                 |                 |
          +-----------------+-----------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
       +-------------+               +-------------+
       |    MySQL    |               |    SMTP     |
       |  Database   |               | Email Server|
       +-------------+               +-------------+
             |                             |
             v                             v
       Application Data             Notifications
       Learning Data               Password Reset
       Security Logs               Reminders


4. TECHNOLOGY STACK
===================

Backend
- Python
- Django
- Django ORM
- Django Authentication

Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

Database
- MySQL

Email
- SMTP
- Django Email Backend

Version Control
- Git
- GitHub

Operating System
- Ubuntu / Linux recommended


5. PROJECT STRUCTURE
====================

Note: Replace <django_project> and <django_app> with the actual directory
names used by the source repository.

lmsmgmt/
|
+-- manage.py
|
+-- <django_project>/
|   +-- __init__.py
|   +-- settings.py
|   +-- urls.py
|   +-- asgi.py
|   +-- wsgi.py
|
+-- <django_app>/
|   +-- __init__.py
|   +-- admin.py
|   +-- apps.py
|   +-- forms.py
|   +-- models.py
|   +-- views.py
|   +-- urls.py
|   +-- signals.py
|   |
|   +-- migrations/
|   |   +-- ...
|   |
|   +-- templates/
|       +-- ...
|
+-- templates/
|   +-- base.html
|   +-- ...
|
+-- static/
|   +-- css/
|   +-- js/
|   +-- images/
|
+-- media/
|
+-- requirements.txt
+-- .gitignore
+-- .env
+-- README.md
+-- INSTALL.md


6. INSTALLATION
===============

6.1 Clone the Repository

Use Git to clone the repository:

    git clone https://github.com/vishnuvm1122/Employee-Learning-Management-System.git

Move into the project directory:

    cd Employee-Learning-Management-System

If your local project directory has a different name, use that directory
instead.


6.2 Check Python

Check the installed Python version:

    python3 --version

Recommended:

    Python 3.x

If Python is not installed:

    sudo apt update
    sudo apt install python3 python3-pip python3-venv -y


6.3 Create a Virtual Environment

    python3 -m venv venv

Activate it:

    source venv/bin/activate

You should see something similar to:

    (venv) user@computer:~/Employee-Learning-Management-System$


6.4 Upgrade pip

    python -m pip install --upgrade pip


6.5 Install Project Dependencies

If the repository contains requirements.txt:

    pip install -r requirements.txt

Verify Django:

    python -m django --version


7. MYSQL INSTALLATION
=====================

Install MySQL on Ubuntu:

    sudo apt update
    sudo apt install mysql-server mysql-client -y

Check MySQL:

    sudo systemctl status mysql

Start MySQL if necessary:

    sudo systemctl start mysql

Enable MySQL at boot:

    sudo systemctl enable mysql


8. CREATE THE DATABASE
======================

Open MySQL:

    sudo mysql

Create the database:

    CREATE DATABASE lmsmgmt
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

Create a dedicated database user:

    CREATE USER 'lmsuser'@'localhost'
    IDENTIFIED BY 'CHANGE_THIS_PASSWORD';

Grant database permissions:

    GRANT ALL PRIVILEGES ON lmsmgmt.* TO 'lmsuser'@'localhost';

Apply privileges:

    FLUSH PRIVILEGES;

Exit MySQL:

    EXIT;

Security:
Replace CHANGE_THIS_PASSWORD with a strong, unique password.


9. DJANGO DATABASE CONFIGURATION
=================================

Open your Django settings.py file.

Example configuration:

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

For production, use environment variables instead of storing database
passwords directly in settings.py.


10. ENVIRONMENT CONFIGURATION
=============================

Create a .env file if the project is configured to use environment
variables:

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

Never upload .env to a public GitHub repository.

Add the following to .gitignore:

    .env


11. RUN DJANGO MIGRATIONS
=========================

Create migrations if required:

    python manage.py makemigrations

Apply migrations:

    python manage.py migrate

Check migration status:

    python manage.py showmigrations


12. CREATE AN ADMINISTRATOR
===========================

Create a Django administrator account:

    python manage.py createsuperuser

Enter the requested:

- Username
- Email
- Password

Use a strong administrator password.


13. COLLECT STATIC FILES
========================

For production:

    python manage.py collectstatic

Ensure these settings are correctly configured:

    STATIC_URL
    STATIC_ROOT
    MEDIA_URL
    MEDIA_ROOT


14. START THE DEVELOPMENT SERVER
================================

Run:

    python manage.py runserver

The application is normally available at:

    http://127.0.0.1:8000/


15. RUN ON A LOCAL NETWORK
==========================

To make the development server accessible from another device:

    python manage.py runserver 0.0.0.0:8000

Then access:

    http://SERVER-IP:8000/

Warning:
Do not use Django's development server as the production web server.


16. ADMIN PANEL
===============

Open:

    /admin/

Example:

    http://127.0.0.1:8000/admin/

Log in using the Django superuser account.


17. EMAIL CONFIGURATION
=======================

The LMS can use SMTP for:

- Password reset emails
- Suspicious login alerts
- Course allocation notifications
- User notifications
- Daily reminders
- Weekly reminders
- System notifications

Example Django configuration:

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = "smtp.example.com"
    EMAIL_PORT = 587

    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False

    EMAIL_HOST_USER = "your-email@example.com"
    EMAIL_HOST_PASSWORD = "your-password"

    DEFAULT_FROM_EMAIL = "your-email@example.com"

For production, store SMTP credentials securely using environment variables.


18. PASSWORD RESET WORKFLOW
===========================

    User
      |
      v
    Forgot Password
      |
      v
    Enter Email
      |
      v
    Django Authentication
      |
      v
    Password Reset Email
      |
      v
    Reset Link
      |
      v
    Create New Password
      |
      v
    Login


19. SECURITY MONITORING
=======================

The LMS includes security-related functionality for monitoring authentication
activity.

Depending on the project configuration, tracked information may include:

- IP address
- Device
- Browser
- Operating system
- User-Agent
- Session
- Login time
- Logout time

Configured security conditions can be used to identify potentially suspicious
login activity.


20. SUSPICIOUS LOGIN NOTIFICATION
=================================

Typical workflow:

    Login
      |
      v
    Capture Login Information
      |
      v
    Security Check
      |
      +-----------------------+
      |                       |
      v                       v
    Normal                Suspicious
      |                       |
      v                       v
    Continue              Log Activity
                              |
                              v
                         Email Alert


21. COURSE MANAGEMENT
=====================

Administrators can manage employee training courses.

Typical workflow:

    Administrator
         |
         v
    Create Course
         |
         v
    Add Course Information
         |
         v
    Save Course
         |
         v
    Allocate Course
         |
         v
    Employee
         |
         v
    Learning
         |
         v
    Progress
         |
         v
    Completion


22. COURSE ALLOCATION
=====================

Course allocation connects employees with their assigned training.

    Employee + Course
           |
           v
    Course Allocation
           |
           v
    Employee Dashboard
           |
           v
    Assigned Course
           |
           v
    Learning


23. LEARNING MANAGEMENT
=======================

Employees can access assigned learning content and track their learning
activities.

Possible learning information includes:

- Assigned courses
- Learning content
- Progress
- Pending activities
- Completed activities
- Course completion


24. NOTIFICATIONS
=================

The system can provide notifications for important events.

Examples:

- Course allocation
- Email notification
- Password reset
- Suspicious login
- Daily reminder
- Weekly reminder
- System notification


25. AUTOMATED REMINDERS
=======================

Daily Reminder

    Employee
       |
       v
    Pending Learning Activity
       |
       v
    Daily Reminder Email


Weekly Reminder

    Employee
       |
       v
    Learning Status
       |
       v
    Weekly Reminder Email

The scheduler configuration should be verified against the actual project
implementation before production deployment.


26. ANDROID APPLICATION SUPPORT
===============================

Where Android integration is enabled, the backend can support application
version management.

Possible version information includes:

- Version name
- Version code
- APK file
- APK size
- Release notes
- Active version
- Force update
- Download count

Version workflow:

    Android App
         |
         v
    Installed Version
         |
         v
    Django Backend
         |
         v
    Version Comparison
         |
       +-+---------+
       |           |
       v           v
     Latest      Update
       |           |
       v           v
    Continue     Download Update


27. TESTING
===========

Run Django's system check:

    python manage.py check

Run tests:

    python manage.py test

Test the following before production.

User Management
- [ ] Create employee
- [ ] Edit employee
- [ ] Activate/deactivate employee
- [ ] Verify permissions

Authentication
- [ ] Login
- [ ] Logout
- [ ] Invalid login
- [ ] Password reset
- [ ] Session handling

LMS
- [ ] Create course
- [ ] Edit course
- [ ] Allocate course
- [ ] Access assigned course
- [ ] Verify progress

Email
- [ ] Password reset email
- [ ] Course notification
- [ ] Suspicious login email
- [ ] Daily reminder
- [ ] Weekly reminder

Security
- [ ] Login activity
- [ ] Logout activity
- [ ] Device information
- [ ] IP information
- [ ] Suspicious login detection


28. PRODUCTION SECURITY CHECKLIST
=================================

Before deploying:

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


29. PRODUCTION ARCHITECTURE
===========================

                    INTERNET
                        |
                        v
                      HTTPS
                        |
                        v
                 +---------------+
                 | Nginx/Apache  |
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | Django / WSGI |
                 +-------+-------+
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          MySQL        SMTP       Android
         Database     Server       Client


30. DATABASE BACKUP
===================

Create a MySQL backup:

    mysqldump -u lmsuser -p lmsmgmt > lmsmgmt_backup.sql

Restore the backup:

    mysql -u lmsuser -p lmsmgmt < lmsmgmt_backup.sql

Store database backups securely and test restoration periodically.


31. PRODUCTION UPDATE COMMANDS
==============================

Activate the virtual environment:

    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Apply migrations:

    python manage.py migrate

Collect static files:

    python manage.py collectstatic

Restart the production application or service as required by the deployment
configuration.


32. TROUBLESHOOTING
===================

No module named django

    source venv/bin/activate
    pip install -r requirements.txt


MySQL Connection Error

Check:

- MySQL service status
- Database name
- Database username
- Database password
- Database host
- Database port

Check MySQL service:

    sudo systemctl status mysql


Missing Database Tables

Run:

    python manage.py makemigrations
    python manage.py migrate


Static Files Not Loading

Run:

    python manage.py collectstatic

Then verify:

    STATIC_URL
    STATIC_ROOT


Email Not Sending

Verify:

- SMTP host
- SMTP port
- SMTP username
- SMTP password
- TLS/SSL configuration
- Firewall rules
- SMTP provider configuration

Also check the spam/junk folder and Django/application logs.


33. USEFUL DJANGO COMMANDS
==========================

Activate virtual environment:

    source venv/bin/activate

Start development server:

    python manage.py runserver

Check project:

    python manage.py check

Create migrations:

    python manage.py makemigrations

Apply migrations:

    python manage.py migrate

Show migrations:

    python manage.py showmigrations

Create administrator:

    python manage.py createsuperuser

Collect static files:

    python manage.py collectstatic

Run tests:

    python manage.py test

Open Django shell:

    python manage.py shell


34. PROJECT OBJECTIVES
======================

The main objectives of this LMS are:

1. Centralize employee management
2. Provide secure authentication
3. Manage employee training courses
4. Simplify course allocation
5. Monitor learning progress
6. Automate email communication
7. Provide notifications and reminders
8. Monitor suspicious authentication activity
9. Track configured login and device activity
10. Support mobile application integration
11. Improve employee training visibility
12. Improve application security


35. FUTURE ENHANCEMENTS
=======================

Potential future improvements include:

- AI-powered learning recommendations
- AI learning assistant
- AI chatbot
- Online examinations
- Quiz management
- Assignment management
- Certificate generation
- Advanced analytics
- Gamification
- Live classes
- Push notifications
- Multi-language support
- Advanced mobile application
- Advanced management reports
- Automated learning recommendations


36. PROJECT STATUS
==================

Status: Active Development

The platform is designed as an extensible Employee Learning Management System
combining:

    User Management
          +
    Authentication
          +
    Course Management
          +
    Course Allocation
          +
    Learning Progress
          +
    Email Management
          +
    Notifications
          +
    Security Monitoring
          +
    Mobile Integration
          =
    Employee Learning Management System


37. DEVELOPMENT
===============

The project is designed to be maintained using:

- Python
- Django
- MySQL
- HTML/CSS
- JavaScript
- Bootstrap
- Git/GitHub
- Linux


38. SECURITY NOTICE
===================

This project handles authentication, employee information, email
configuration, and security-related activity.

For production deployments:

- Never commit passwords.
- Never commit .env files.
- Never expose the Django SECRET_KEY.
- Use HTTPS.
- Use strong administrator passwords.
- Keep dependencies updated.
- Configure database backups.
- Restrict administrative access.
- Review application logs regularly.
- Follow the security requirements of your organization.

Only perform security testing against systems and accounts that you own or
have explicit authorization to test.


39. LICENSE
===========

Add the organization's license information here.

Example:

    MIT License

Replace the example with the actual license used by the project.


40. SUPPORT
===========

For project-related support, configuration, deployment, or development
questions, contact the project administrator or development team.


PROJECT LINKS
=============

GitHub Repository:

vishnuvm1122/Employee-Learning-Management-System.git

LinkedIn:
https://www.linkedin.com/in/vishnuvm1997/


EMPLOYEE LEARNING MANAGEMENT SYSTEM
===================================

Secure | Organized | Scalable | Employee-Focused

Built with Python and Django
'''

path = Path("/mnt/data/Employee_Learning_Management_System_README.txt")
path.write_text(content, encoding="utf-8")
print(path)
  convert to github reme.md model add icoms and emojies

Data analysis isn't available right now. Do you want to continue without it? 

Data analysis will be available again when usage resets after 2:42 PM. Upgrade now for expanded access and advanced intelligence.
Upgrade to Plus




from pathlib import Path

content = r'''# 🎓 Employee Learning Management System (LMS)

<p align="center">

### 🚀 Secure • Scalable • Employee-Focused Learning Platform

A complete web-based Learning Management System built with **Python, Django,
MySQL, HTML5, CSS3, JavaScript, and Bootstrap** for managing employees,
courses, course allocations, learning activities, notifications, email
communication, and security monitoring.

</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Framework-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-Frontend-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)

</p>

---

## 📌 Table of Contents

- [🌟 Project Overview](#-project-overview)
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
- [📊 Learning Management](#-learning-management)
- [🔔 Notifications & Reminders](#-notifications--reminders)
- [📱 Android Application Support](#-android-application-support)
- [🧪 Testing](#-testing)
- [🔒 Production Security](#-production-security)
- [💾 Database Backup](#-database-backup)
- [🩺 Troubleshooting](#-troubleshooting)
- [📋 Useful Django Commands](#-useful-django-commands)
- [🎯 Project Objectives](#-project-objectives)
- [🌟 Future Enhancements](#-future-enhancements)
- [📈 Project Status](#-project-status)
- [📄 License](#-license)
- [🔗 Project Links](#-project-links)

---

## 🌟 Project Overview

The **Employee Learning Management System (LMS)** is a centralized platform
designed to manage employee training, learning activities, course allocation,
notifications, email communication, and authentication monitoring.

### 👨‍💼 Administration

Administrators can:

- 👤 Create and manage employee accounts
- 🔐 Manage authentication and access
- 📚 Create and manage courses
- 🎯 Allocate courses to employees
- 📊 Monitor learning progress
- 📧 Configure email services
- 🔔 Manage notifications
- 📅 Configure learning reminders
- 🛡️ Monitor login/logout activity
- 💻 Track configured device/session information
- 🚨 Detect configured suspicious login activity
- 📱 Manage Android application versions
- 📦 Manage APK releases and downloads

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 👤 **User Management** | Create, edit, activate, deactivate, and manage employee accounts |
| 🔐 **Authentication** | Secure login and logout functionality |
| 🔑 **Password Reset** | Forgot-password and password-reset workflow |
| 📚 **Course Management** | Create and manage employee training courses |
| 🎯 **Course Allocation** | Assign courses to employees |
| 📊 **Progress Tracking** | Monitor employee learning progress and completion |
| 📧 **Email Settings** | Configure SMTP/email services |
| 🔔 **Notifications** | Application and email notifications |
| 📅 **Daily Reminders** | Automated daily learning reminders |
| 📆 **Weekly Reminders** | Automated weekly learning reminders |
| 🛡️ **Security Monitoring** | Monitor authentication activity |
| 💻 **Device Tracking** | Record configured device and browser information |
| 🌐 **IP Tracking** | Record login IP information |
| 🚨 **Suspicious Login Detection** | Detect configured suspicious authentication activity |
| 📱 **Android Integration** | Support Android application/version management |
| 📦 **APK Management** | Manage APK versions, releases, and downloads |
| 👨‍💼 **Admin Dashboard** | Centralized administration |
| 🗄️ **MySQL Database** | Relational database support |

---

## 🏗️ System Architecture

```text
                         🌐 USER
                            │
                            ▼
                  ┌───────────────────┐
                  │   🌍 Web Browser   │
                  │ HTML5 / CSS3 / JS │
                  │    Bootstrap      │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    🐍 Django      │
                  │     Backend       │
                  └─────────┬─────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
   👤 User Management    📚 LMS          🛡️ Security
          │                 │                 │
          ▼                 ▼                 ▼
   🔐 Authentication   📖 Courses       🔐 Login Monitoring
   👥 User Creation    🎯 Allocation    💻 Device Tracking
   🔑 Permissions      📊 Progress      🚨 Suspicious Login
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       ┌─────────────┐               ┌─────────────┐
       │ 🗄️ MySQL    │               │ 📧 SMTP     │
       │  Database   │               │ Email Server│
       └─────────────┘               └─────────────┘
             │                             │
             ▼                             ▼
       Application Data             🔔 Notifications
       Learning Data                🔑 Password Reset
       Security Logs                📅 Reminders
🛠️ Technology Stack
🐍 Backend
Python
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

ℹ️ Replace <django_project> and <django_app> with the actual names used
by the source repository.

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

Move into the project directory:

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
5️⃣ Install Dependencies

If requirements.txt is available:

pip install -r requirements.txt

Verify Django:

python -m django --version
🐬 MySQL Setup
6️⃣ Install MySQL

On Ubuntu:

sudo apt update
sudo apt install mysql-server mysql-client -y

Check MySQL:

sudo systemctl status mysql

Start MySQL if necessary:

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

⚠️ Security: Replace CHANGE_THIS_PASSWORD with a strong, unique
password.

⚙️ Django Configuration
8️⃣ Configure the Database

Open your Django settings.py.

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

🔐 For production, use environment variables instead of storing passwords
directly in settings.py.

9️⃣ Environment Variables

Create a .env file if the project uses environment variables:

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

Never commit .env to GitHub.

Add it to .gitignore:

.env
*.pyc
__pycache__/
venv/
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

Use a strong administrator password.

🎨 Static Files
1️⃣2️⃣ Collect Static Files

For production:

python manage.py collectstatic

Verify these settings:

STATIC_URL
STATIC_ROOT
MEDIA_URL
MEDIA_ROOT
▶️ Run the Application
1️⃣3️⃣ Start Development Server
python manage.py runserver

The application is normally available at:

http://127.0.0.1:8000/
🌐 Run on a Local Network

To make the development server accessible from another device:

python manage.py runserver 0.0.0.0:8000

Then access:

http://SERVER-IP:8000/

⚠️ Do not use Django's development server as the production web server.

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

Example Django configuration:

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = "your-email@example.com"
EMAIL_HOST_PASSWORD = "your-password"

DEFAULT_FROM_EMAIL = "your-email@example.com"

🔐 For production, store SMTP credentials securely using environment
variables or a secret-management system.

🔐 Authentication
Password Reset Workflow
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
💻 Device
🌍 Browser
🖥️ Operating system
🧾 User-Agent
🔐 Session information
🕐 Login time
🕐 Logout time

Configured security conditions can be used to identify potentially suspicious
login activity.

🔒 Ensure that security and employee data collection follows applicable
organizational policies and privacy requirements.

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
✅ Completion
🎯 Course Allocation

Course allocation connects employees with assigned training.

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
📧 Email notification
🔑 Password reset
🚨 Suspicious login
📅 Daily reminder
📆 Weekly reminder
⚙️ System notification
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

Possible version information:

🏷️ Version name
🔢 Version code
📦 APK file
📏 APK size
📝 Release notes
🟢 Active version
🔄 Force update
📥 Download count
Android Version Workflow
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

Run tests:

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
🔒 Production Security

Before deploying to production:

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
🔐 Security Best Practices
Never commit passwords.
Never commit .env files.
Never expose the Django SECRET_KEY.
Use HTTPS in production.
Use strong administrator passwords.
Keep dependencies updated.
Configure regular database backups.
Restrict administrative access.
Review application logs regularly.
Follow organizational privacy and security requirements.
🚀 Production Architecture
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
💾 Database Backup

Create a MySQL backup:

mysqldump -u lmsuser -p lmsmgmt > lmsmgmt_backup.sql

Restore the backup:

mysql -u lmsuser -p lmsmgmt < lmsmgmt_backup.sql

💡 Store database backups securely and test restoration periodically.

🔄 Production Update

Activate the environment:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Collect static files:

python manage.py collectstatic

Restart the production application or service according to your deployment
configuration.

🩺 Troubleshooting
❌ No module named django
source venv/bin/activate
pip install -r requirements.txt
🐬 MySQL Connection Error

Check:

sudo systemctl status mysql

Verify:

Database name
Database username
Database password
Database host
Database port
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
📧 Email Not Sending

Verify:

SMTP Host
SMTP Port
SMTP Username
SMTP Password
TLS / SSL configuration
Firewall
SMTP Provider

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
🚨 Monitor suspicious authentication activity
💻 Track configured login/device activity
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
🎨 HTML / CSS
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
📜 Follow applicable organizational security and privacy requirements.

Only perform security testing against systems and accounts that you own or
have explicit authorization to test.

📄 License

Add the organization's license information here.

Example:

MIT License

Replace the example with the actual license used by the project.

🔗 Project Links
🐙 GitHub Repository

https://github.com/vishnuvm1122/Employee-Learning-Management-System.git

💼 LinkedIn

https://www.linkedin.com/in/vishnuvm1997/

<p align="center">
🎓 Employee Learning Management System
🔐 Secure • 📚 Organized • 🚀 Scalable • 👨‍💼 Employee-Focused

Built with 🐍 Python & 🌐 Django

</p> 
