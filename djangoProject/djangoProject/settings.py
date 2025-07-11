from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGOUT_REDIRECT_URL = '/login/'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# For development: directories where Django looks for static files
STATICFILES_DIRS = [
    BASE_DIR / "login/static",
    BASE_DIR / "djangoProject/static",
]

# For production: directory where collectstatic will gather static files
STATIC_ROOT = BASE_DIR / "staticfiles"  # Note the folder name changed to 'staticfiles'

# Use WhiteNoise for serving static files in production
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-pqt^2-hh9l@^bwufrq0)ej6+uoat_4qq4qf*u+safw9htwx8jg"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False  # Set to False for production

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'healthcare-portal-zkt4.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    "sharedModels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "login",
    "landing",
    "schedule",
    "equipment",
    "lab_order",
    "pharmacy",
    "patient_record",
    "insurance",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add WhiteNoise middleware here
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'djangoProject' / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "djangoProject.wsgi.app"  # If your wsgi.py has 'app', keep this as is

# Database (SQLite for now)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
