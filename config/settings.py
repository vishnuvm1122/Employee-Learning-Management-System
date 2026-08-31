from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# ---------------- BASE DIR ----------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------- SECURITY ----------------
SECRET_KEY = 'django-insecure-change-this-key'
DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',                # localhost
    'localhost', 
]


# ---------------- CUSTOM USER ----------------
AUTH_USER_MODEL = 'accounts.User'


# ---------------- INTERNATIONALIZATION & LANGUAGES ----------------
USE_I18N = True
USE_TZ = True

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

LANGUAGES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('ta', 'Tamil'),
    ('ml', 'Malayalam'),
    ('kn', 'Kannada'),
    ('te', 'Telugu'),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# ---------------- CSRF & SECURITY HEADERS ----------------
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_DOMAIN = None

SESSION_COOKIE_SECURE = False

SECURE_SSL_REDIRECT = False

SECURE_PROXY_SSL_HEADER = None

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://localhost:8000",
    "https://127.0.0.1:8000",
]


# ---------------- INSTALLED APPS ----------------
DJANGO_APPS = [
    'jazzmin',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "django_filters",
    "import_export",
]

PROJECT_APPS = [
    "accounts",   # ✅ MUST COME FIRST (important for custom user)
    "core",
    "course",
    "quiz",
    "courseallocations",
    "emailsettings",
    "results",
    "search",
    "notifications",
    "channels",
    "feedback",
    "android",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


# ---------------- AUTHENTICATION URLS ----------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"


# ---------------- MIDDLEWARE ----------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.SuperuserAdminOnlyMiddleware',
    'accounts.middleware.MaintenanceModeMiddleware',
    'accounts.middleware.SessionTimeoutMiddleware',
    'accounts.middleware.LoginRestrictionMiddleware',
    'accounts.middleware.AuditMiddleware',
]


# ---------------- URLS & WSGI/ASGI ----------------
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = "core.asgi.application"


# ---------------- TEMPLATES ----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ---------------- CHANNELS ----------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# ---------------- DATABASE ----------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------- PASSWORD VALIDATION ----------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ---------------- STATIC & MEDIA FILES ----------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static' 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ---------------- CRISPY FORMS ----------------
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"


# ---------------- DEFAULT FIELD ----------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------------------
# Jazzmin Settings
# -------------------------
JAZZMIN_SETTINGS = {
    "site_title": "LMS Admin",
    "site_header": "Learning Management System",
    "site_brand": "LMS",
    "welcome_sign": "Welcome to the LMS Admin Panel",
    "copyright": "LMS © 2026",
    "search_model": "accounts.User",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth.User": "fas fa-user-circle",
        "accounts.User": "fas fa-user-circle",
        "course.Course": "fas fa-book-open",
        "courseallocations.CourseAllocation": "fas fa-tasks",
        "email_app.EmailSettings": "fas fa-envelope-open-text",
        "accounts.DepartmentHead": "fas fa-chess-king",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": None,
    "custom_js": None,
    "topmenu_links": [
        {"name": "Home", "url": "/", "new_window": False},
        {"name": "Docs", "url": "https://docs.djangoproject.com/", "new_window": True},
        {"name": "Reports", "url": "/admin/reports/", "new_window": False},
    ],
}

# -------------------------
# Jazzmin UI Tweaks (Red Theme)
# -------------------------
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": None,
    "accent": "danger",
    "navbar_fixed": True,
    "footer_fixed": True,
    "show_ui_builder": True,
    "form_label_upper": True,
    "changeform_format": "collapsible-tabs",
    "card_classes": {
        "User": "card-danger",
        "CourseAllocation": "card-danger",
        "EmailSettings": "card-danger",
        "DepartmentHead": "card-danger",
    },
}

# -------------------------
# Optional Django admin header titles
# -------------------------
ADMIN_SITE_HEADER = "LMS Administration"
ADMIN_SITE_TITLE = "LMS Admin"
ADMIN_INDEX_TITLE = "Dashboard"