import os
from pathlib import Path
from mongoengine import connect
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-%&z=s7yj42xb4k1ncgut^yi)cwe3hqmpo5&7iv0oy6w1xn@+bf'

DEBUG = False
# DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'api',
    'corsheaders',
    'rest_framework',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework.authtoken',
    'users',
    'pictures',
    'chatbot',
    'onthisdate',
    'authentication',
    'verification',
    'chat',
    'channels',
    'rest_framework_simplejwt',
    'news',
]

SITE_ID = 1 
# LOGIN_URL = '/api/auth/google/login/'
LOGIN_REDIRECT_URL = '/api/auth/google/callback/'


# CORS settings
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",  # React frontend
]
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'astrocap_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# GenAi
SECRET_KEY = 'AIzaSyD3lNxKVfPt62OQaXlfwqEIkmiWN_YMrxw'

WSGI_APPLICATION = 'astrocap_app.wsgi.application'

# session
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Stores sessions in DB

# Ensure chatbot sessions persist
SESSION_COOKIE_AGE = 3600  # 1 hour session duration
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False  # Set to True in production
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

connect("astro_cap", host="mongodb://localhost:27017/astro_cap") 
# connect("astro_cap", host="mongodb://localhost:27017/astro_cap") 
DATABASES = {} 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWS_CREDENTIALS = True

AUTHENTICATION_BACKENDS = ( 
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'authentication.backends.MongoEngineBackend',
)

# Google OAuth settings
GOOGLE_CLIENT_ID = '760928481598-omlj3g6vbou13kd7shbm8geijookhv30.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
BASE_URL = 'http://localhost:8000'
FRONTEND_URL = 'http://localhost:3000'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '760928481598-omlj3g6vbou13kd7shbm8geijookhv30.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    }
}

SOCIALACCOUNT_STORE_TOKENS = True 

ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = True


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/build/static"),
]

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Or 'amqp://guest:guest@localhost:5672/' for RabbitMQ
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Optional, for storing task results
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'IST'  

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '21pw07@psgtech.ac.in'
EMAIL_HOST_PASSWORD = 'janu21pw07'
EMAIL_FROM = '21pw07@psgtech.ac.in'

# Channels settings
ASGI_APPLICATION = 'astrocap_app.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}
