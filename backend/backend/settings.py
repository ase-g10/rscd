"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import Config, RepositoryEnv
import os, sys
# import rest_framework_simplejwt

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_file = os.path.join(BASE_DIR.parent, '.env')
if os.path.isfile(env_file):
    config = Config(RepositoryEnv(env_file))
else:
    config = Config(os.environ)
#TODO:这里改成ASE_GROUP10
sys.path.insert(0, os.path.join(BASE_DIR, 'backend'))
ENV = config('DJANGO_ENV')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY',
                    default='9owxyeo8(==0popen%%yv2=o69no61z*8&xkqdgrhdd#v%r)vr6_d=+ykndcdqx0rm&7-tm7!c_rr(7x!rh@c6$h&8n91_0yaqx7')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)
CORS_ORIGIN_ALLOW_ALL = True
# 实际请求所允许的请求方式列表。默认为：
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
# 发出实际请求时可以使用的非标准HTTP标头的列表。默认为:
CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# url结尾自动加/
APPEND_SLASH = True  # 默认是True

ALLOWED_HOSTS = [ "rscdapi.iocky.com", "localhost", "127.0.0.1",
                 config('DJANGO_DB_HOST', default='localhost'), "rscdapistaging.iocky.com" ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'social_django',
    'corsheaders',
    'models',
    'traffic_management',
    'notification_management',
    'disaster_management',
    'emergency_team_management',
    'channels',
]

ASGI_APPLICATION = 'backend.routing.application'

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
#TODO: 这里要改成“ASE_Group10.urls”
ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

#TODO: 这里要改成“ASE_Group10.wsgi.application”
WSGI_APPLICATION = 'backend.wsgi.application'
SOCIAL_AUTH_GITHUB_KEY = config('DJANGO_GITHUB_CLIENT_ID', default='98a50d02de2c591daac8')
SOCIAL_AUTH_GITHUB_SECRET = config('DJANGO_GITHUB_CLIENT_SECRET', default='test')
SOCIAL_AUTH_GITHUB_REDIRECT_URI = config('DJANGO_GITHUB_REDIRECT_URI',
                                         default='http://localhost:8000/dr/api/auth2/github_callback')
FRONT_END_URL = config('DJANGO_FRONT_END_URL', default='http://localhost:8080/#')

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if ENV == 'test':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            'TEST': {
                'NAME': BASE_DIR / "test_db.sqlite3",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('DJANGO_DB_NAME', default='rscd_test_only'),
            'USER': config('DJANGO_DB_USER', default='rscd_test_only'),
            'PASSWORD': config('DJANGO_DB_PASSWORD', default='IjiaDGpeQNPd6EvyI7lRPqwHgxVlGg46'),
            'HOST': config('DJANGO_DB_HOST', default='localhost'),
            'PORT': config('DJANGO_DB_PORT', default='3306'),
        }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Our user model
AUTH_USER_MODEL = 'models.User'

CSRF_TRUSTED_ORIGINS=['https://*.iocky.com']