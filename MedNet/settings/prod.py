from .base import *


DEBUG = config('PROD_DEBUG', cast=bool)
SERVER_PORT = 8080
DATABASES = {
    'default': {
        'ENGINE': config('PROD_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
    }
}
