# Production Settings Config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('ATSTS9_SECRET_KEY')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.squaresandcubes.net',
    '3.14.29.91',
    '172.31.16.108'
]


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sts9_3',
        'USER': 'admin',
        'PASSWORD': os.environ.get('ATSTS9_DB_PWD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True