"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['freelanze.tk', '54.249.247.138']


# Application definition

INSTALLED_APPS = [
    'register.apps.RegisterConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django_cleanup',
    'django_ses',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '.czhr67wuwire.ap-northeast-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'sql_mode': 'TRADITIONAL,NO_AUTO_VALUE_ON_ZERO,ONLY_FULL_GROUP_BY',
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

#カスタムユーザーモデル読み込み
AUTH_USER_MODEL = 'register.User'


LOGIN_URL = 'register:login'
LOGIN_REDIRECT_URL = 'register:top'
LOGOUT_REDIRECT_URL = 'register:top'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'register:top' # リダイレクトURL


AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
 'social_core.backends.twitter.TwitterOAuth',  #for Twitter
 'social_core.backends.instagram.InstagramOAuth2', #for Instagram
 'social_core.backends.facebook.FacebookOAuth2',
 'social_core.backends.github.GithubOAuth2',
 'django.contrib.auth.backends.ModelBackend',
)


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' #Paste Secret Key
SOCIAL_AUTH_TWITTER_KEY = '' #Consumer Key (API Key)
SOCIAL_AUTH_TWITTER_SECRET = '' # Consumer Secret (API Secret)
SOCIAL_AUTH_FACEBOOK_KEY = ''  # アプリID
SOCIAL_AUTH_FACEBOOK_SECRET = ''  # app secret
SOCIAL_AUTH_GITHUB_KEY = '' # Client ID
SOCIAL_AUTH_GITHUB_SECRET = '' # Client Secret


"""AWS設定軍"""

"""IAM"""
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

"""SES"""
EMAIL_BACKEND = 'django_ses.SESBackend'  # バックエンドをSESに変更
AWS_SES_REGION_NAME = 'ap-northeast-1'
AWS_SES_REGION_ENDPOINT = 'email.ap-northeast-1.amazonaws.com'
DEFAULT_FROM_EMAIL = SERVER_EMAIL = 'freelanze <@gmail.com>'

"""S3"""
AWS_STORAGE_BUCKET_NAME = 'aws-s3-freelanze'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_DIRS = (
    [
        os.path.join(BASE_DIR, "static"),
    ]
)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
