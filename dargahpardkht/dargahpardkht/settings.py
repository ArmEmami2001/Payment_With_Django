import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / '.env'


load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = True

ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ninja_jwt',
    'ninja_extra',
    'creditpurchase',
    "azbankgateways",
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dargahpardkht.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dargahpardkht.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from datetime import timedelta

NINJA_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}


AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
      
        "ZARINPAL": {
            "MERCHANT_CODE": os.getenv("MERCHANT_CODE"),
            "SANDBOX": 1,  # 0 disable, 1 active
            "IS_ENABLED": True,
        },
      
    },
    "IS_SAMPLE_FORM_ENABLE": False,  # اختیاری و پیش فرض غیر فعال است
    "DEFAULT": "ZARINPAL",
    "CURRENCY": "IRR",  # اختیاری
    "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
    "TRACKING_CODE_LENGTH": 16,  # اختیاری
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",  # اختیاری
    "BANK_PRIORITIES": [
        "ZARINPAL",

    ],  
    "IS_SAFE_GET_GATEWAY_PAYMENT": False,  # اختیاری، بهتر است True بزارید.
    "CUSTOM_APP": None,  # اختیاری
}
CORS_ALLOWED_ORIGINS = [
         "http://localhost:5173", 
         "https://localhost:5173", 
     ]
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173", "https://localhost:5173"]