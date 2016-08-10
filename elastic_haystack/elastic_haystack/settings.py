"""
Django settings for elastic_haystack project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!7z9h_mkv)4g!5v(_e%xm#wcgg12qg4z__=*!7a^*29^1v*5qi'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'haystack',
    'basesearch',
    'elastic_haystack',
    'rest_framework',
    'drf_haystack',

)
# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'




HAYSTACK_DEFAULT_OPERATOR = 'AND'



MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'elastic_haystack.urls'

WSGI_APPLICATION = 'elastic_haystack.wsgi.application'

# ELASTICSEARCH_INDEX_SETTINGS ={
#             "settings": {
#                 "analysis": {
#                     "analyzer": {
#                          "ik_max_word": {
#                              "type": "ik",
#                              "tokenizer": "ik_max_word",
#                              "filter": "standard"
#                          },
#                         "ngram_analyzer": {
#                             "type": "custom",
#                             "tokenizer": "lowercase",
#                             "filter": ["haystack_ngram"]
#                         },
#                         "edgengram_analyzer": {
#                             "type": "custom",
#                             "tokenizer": "lowercase",
#                             "filter": ["haystack_edgengram"]
#                         }
#                     },
#                     "tokenizer": {
#                         "haystack_ngram_tokenizer": {
#                             "type": "nGram",
#                             "min_gram": 1,  #3
#                             "max_gram": 1,
#                         },
#                         "haystack_edgengram_tokenizer": {
#                             "type": "edgeNGram",
#                             "min_gram": 1,  #2
#                             "max_gram": 1,
#                             "side": "front"
#                         }
#                     },
#                     "filter": {
#                         "haystack_ngram": {
#                             "type": "nGram",
#                             "min_gram": 1,  #3
#                             "max_gram": 1
#                         },
#                         "haystack_edgengram": {
#                             "type": "edgeNGram",
#                             "min_gram": 1,   #2
#                             "max_gram": 1
#                         }
#                     }
#                 }
#             }
#         }

ELASTICSEARCH_INDEX_SETTINGS ={
            "settings": {
                "analysis": {
                    "analyzer": {
                         "ik_max_word": {
                             "type": "ik",
                             "tokenizer": "ik_max_word",
                             "filter": "standard"
                         },
                    }

                }
            }
        }


ELASTICSEARCH_DEFAULT_ANALYZER = "ik_max_word"
# ELASTICSEARCH_DEFAULT_ANALYZER = "mmseg"




HAYSTACK_CONNECTIONS = {
    'default': {
       # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'ENGINE': 'elastic_haystack.utils.ConfigurableElasticSearchEngine',
        'INCLUDE_SPELLING': True,
        'URL': 'http://127.0.0.1:9200/',

        'INDEX_NAME': 'elastic-data1',
    },
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'djangodb',                      # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': 'southcn',
        'HOST': '172.18.9.64',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

HAYSTACK_CUSTOM_HIGHLIGHTER='elastic_haystack.utils.CustomHighlighter'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

