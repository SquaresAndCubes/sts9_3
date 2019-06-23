#Development Settings Config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3ehjhf@s9@mtkp%1j_v$nz2t4e(ce_t%=f61oee35hw+8zik!d'


ALLOWED_HOSTS = [
    'testserver',
    'localhost',
    '127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sts9_3',
        'USER': 'admin',
        'PASSWORD': os.environ.get('ATSTS9_DB_PWD'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
