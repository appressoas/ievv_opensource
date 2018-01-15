# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django_dbdev.backends.postgres import DBSETTINGS

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)))))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y%j0x%=7a^sf53m*s^5nbmfe0_t13d*oibfx#m#*wz1x+k6+m1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': DBSETTINGS
}
DATABASES['default']['PORT'] = 23653


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'django_rq',
    'sorl.thumbnail',
    'django_dbdev',
    'crispy_forms',
    'django_cradmin',
    'django_cradmin.apps.cradmin_authenticate',
    'django_cradmin.apps.cradmin_temporaryfileuploadstore',
    'ievv_opensource.ievv_tagframework',
    'ievv_opensource.ievv_batchframework',
    'ievv_opensource.demo.demoapp',
    'ievv_opensource.demo.demoapp2',
    'ievv_opensource.demo.customsqldemo',
    'ievv_opensource.demo.batchframeworkdemo.apps.BatchFrameworkDemoAppConfig',
    'ievv_opensource.ievvtasks_common',
    'ievv_opensource.ievvtasks_development',
    'ievv_opensource.ievvtasks_production',
    'ievv_opensource.ievv_elasticsearch',
    'ievv_opensource.ievv_elasticsearch2.apps.IevvElasticSearch2AppConfig',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': True,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'django_cradmin.context_processors.cradmin',
            ],
        },
    },
]

ROOT_URLCONF = 'django_cradmin.demo.project.demo.urls'

# Sorl-thumbnail settings
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
THUMBNAIL_PREFIX = 'sorlcache/'
THUMBNAIL_DEBUG = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# The root for file fileuploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'django_media_root')
STATIC_ROOT = os.path.join(BASE_DIR, 'django_static_root')

MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(name)s %(pathname)s:%(lineno)s] %(message)s'
        },
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stderr': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler'
        },
        "rq_console": {
            "level": "DEBUG",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['stderr'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.db': {
            'handlers': ['stderr'],
            'level': 'INFO',  # Do not set to debug - logs all queries
            'propagate': False
        },
        'elasticsearch': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': False
        },
        'urllib3': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': False
        },
        'sh': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': False
        },
        "rq.worker": {
            "handlers": ["rq_console"],
            "level": "DEBUG"
        },
        '': {
            'handlers': ['stderr'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Use bootstrap3 template pack to django-crispy-forms.
CRISPY_TEMPLATE_PACK = 'bootstrap3'


IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES = [
    'en',
    'nb',
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES = [
    ('example-tagtype1', 'Example tagtype 1'),
    ('example-tagtype2', 'Example tagtype 2'),
]

IEVVTASKS_DOCS_DASH_NAME = 'ievv_opensource'

# Redis broker
BROKER_URL = 'redis://localhost:6381'

# RQ queue setup.
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6381,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'highpriority': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6381/0'),  # If you're on Heroku
        'DEFAULT_TIMEOUT': 500,
    },
}