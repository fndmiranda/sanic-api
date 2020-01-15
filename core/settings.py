from decouple import config

SECRET_KEY = config('SECRET_KEY', default='secret', cast=str)
DEBUG = config('DEBUG', default=False, cast=bool)
ASYNC = config('ASYNC', default=True, cast=bool)
HOST = config('HOST', default='0.0.0.0', cast=str)
PORT = config('PORT', default=8000, cast=int)
DATABASE_URL = config('DATABASE_URL', default='sqlite:///database.sqlite', cast=str)
