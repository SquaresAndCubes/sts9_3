# Production Settings Config

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'x^fq0^@&!@zw_nnwm4x32a)gbg@5y4bb$qw(7n0cnft%m(jr*y'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# google social auth keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '257995102785-enp3j1gbn1ot4qm1lma558iu5ced6i7r.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'z_Bx5lguAThJ7_RpGjHKHj1c'
# facebook social auth keys
SOCIAL_AUTH_FACEBOOK_KEY = '688722228179914'
SOCIAL_AUTH_FACEBOOK_SECRET = 'd38ec5eda6b23ac4600ed891a1507c21'
# twitter social auth keys
SOCIAL_AUTH_TWITTER_KEY = '0GdFEsFWQtjPSzDUD3b6igb0j'
SOCIAL_AUTH_TWITTER_SECRET = 'J7Pa7VtdidZkckx5KuAt6yXqWFuEgSpZczgITsR7tCTIyqakZv'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sts9_3',
        'USER': 'admin',
        'PASSWORD': 'sts9db',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
