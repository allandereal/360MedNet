from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

DATABASES = {
    'default': {
        'ENGINE': config('DEV_ENGINE'),
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
