from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)
SERVER_PORT = 8009
DATABASES = {
    'default': {
        'ENGINE': config('PROD_ENGINE'),
        'NAME': config('DB_NAME_DEV'),
        'USER': config('DB_USER'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}
