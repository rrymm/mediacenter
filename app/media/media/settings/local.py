from media.settings.base import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        # django.db.backends.postgresql_psycopg2
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mediacenter',
        'USER': 'mediacenter',
        'PASSWORD': 'test123',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TURN_SECRET = b'mediacenterSECRET'

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
    '127.0.0.1:8080'
)
