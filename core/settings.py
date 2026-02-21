"""
Django settings for core project.
"""

from datetime import timedelta
from pathlib import Path
from urllib.parse import unquote, urlparse

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me-in-production")

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"

# Database configuration from environment
DATABASE_URL = config("DATABASE_URL", default="sqlite:///db.sqlite3")
parsed_db_url = urlparse(DATABASE_URL)

if parsed_db_url.scheme == "sqlite":
    db_path = unquote(parsed_db_url.path or "")
    if not db_path or db_path == "/":
        db_name = BASE_DIR / "db.sqlite3"
    elif db_path.startswith("/"):
        db_name = Path(db_path)
    else:
        db_name = BASE_DIR / db_path
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": db_name,
        }
    }
elif parsed_db_url.scheme in {"postgresql", "postgres"}:
    if parsed_db_url.hostname and parsed_db_url.path and parsed_db_url.path != "/":
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": parsed_db_url.path.lstrip("/"),
                "USER": unquote(parsed_db_url.username or ""),
                "PASSWORD": unquote(parsed_db_url.password or ""),
                "HOST": parsed_db_url.hostname,
                "PORT": parsed_db_url.port or 5432,
            }
        }
    else:
        raise ValueError(f"Invalid PostgreSQL DATABASE_URL format: {DATABASE_URL}")
elif parsed_db_url.scheme in {"mysql", "mysql2"}:
    if parsed_db_url.hostname and parsed_db_url.path and parsed_db_url.path != "/":
        mysql_db_name = parsed_db_url.path.lstrip("/")
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": mysql_db_name,
                "USER": unquote(parsed_db_url.username or ""),
                "PASSWORD": unquote(parsed_db_url.password or ""),
                "HOST": parsed_db_url.hostname,
                "PORT": parsed_db_url.port or 3306,
                "OPTIONS": {"charset": "utf8mb4"},
                "TEST": {"NAME": f"test_{mysql_db_name}"},
            }
        }
    else:
        raise ValueError(f"Invalid MySQL DATABASE_URL format: {DATABASE_URL}")
else:
    raise ValueError(f"Unsupported DATABASE_URL format: {DATABASE_URL}")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JTI_CLAIM": "jti",
}

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001",
    cast=lambda v: [s.strip() for s in v.split(",")],
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    default="http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001",
    cast=lambda v: [s.strip() for s in v.split(",")],
)


AUTH_USER_MODEL = "api.CustomUser"
