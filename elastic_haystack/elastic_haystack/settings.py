# -*- coding:utf-8 -*-
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
    'elasticsearch',
    # 'elastic_haystack',

    'raven.contrib.django.raven_compat',

)



ELASTICSEARCH_DEFAULT_ANALYZER='index_ansj'

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




Fields_Mapping  = {
    'title': 'index_ansj',
    'content': 'index_ansj',
    # 'INDEXNUM': 'index_ansj',
    # 'MENUCAT': 'index_ansj',
    # 'FILENUM': 'standard',
    # 'ORGANCAT': 'index_ansj',
    # 'KEYWORDS': 'index_ansj',
    # 'TITLE': 'index_ansj',
    # 'CONTENT': 'index_ansj',
    # 'DESCRIPTION': 'index_ansj',
    # 'APPENDIXS': 'index_ansj',
    # 'URL': 'standard',
    # 'PUBLISHER': 'whitespace',
    'autolink': 'standard',
    # 'clear_indexnum': 'index_ansj',
    # 'clear_publisher': 'whitespace',  # 发布单位分级,用/隔开 采用path_hierachy
    # 'provincial_office': 'standard',
}


# Custom_Score = ""

# Custom_Score = "degree1 = doc['degree'].value-10956;degree2 = doc['degree'].value+10956;return _score*1 + degree1/degree2*100;"

Custom_Score = "if (_score > 2) { return 5 } else {return 1} "

"""
a=doc['degree'].value-25245;b=2000-pow(a,2)/1000;return b*1+_score*1

"""


HAYSTACK_CONNECTIONS = {
    'default': {
       #  'ENGINE': 'elastic_haystack.utils.ConfigurableElasticSearchEngine',
       #  'ENGINE' : 'basesearch.search_backends.ConfigurableElasticSearchEngine2',
        'ENGINE':'basesearch.elasticsearch_2.Elasticsearch2SearchEngine',
        'INCLUDE_SPELLING': True,
        # 'URL': 'http://127.0.0.1:9200/',
        'URL': 'http://172.18.9.65:9200/',
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

TIME_ZONE = 'Asia/Chongqing'

USE_I18N = False

USE_L10N = False

USE_TZ = False

HAYSTACK_CUSTOM_HIGHLIGHTER = 'basesearch.customhighlighter.CustomHighlighter'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/



STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

import raven
RAVEN_CONFIG = {
    'dsn': 'http://29d35de6a2fb4884981cc516ae517ea1:1ee904e8267d45a18a94f10f5696093c@10.0.0.41/5',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}