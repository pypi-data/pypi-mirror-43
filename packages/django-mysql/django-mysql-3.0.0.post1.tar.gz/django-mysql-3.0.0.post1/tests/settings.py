import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'THISuISdNOT9A$SECRET9x&ji!vceayg+wwt472!bgs$0!i3k4'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_mysql',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
            # The most forward compatible sql_mode, for 5.7
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,"
                            "NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,"
                            "NO_AUTO_CREATE_USER', innodb_strict_mode=1",
        },
        'TEST': {
            'COLLATION': "utf8mb4_general_ci",
            'CHARSET': "utf8mb4",
        },
    },
    'other': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_mysql2',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'charset': 'utf8mb4',
            # The most forward compatible sql_mode, for 5.7
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,"
                            "NO_ZERO_IN_DATE,ERROR_FOR_DIVISION_BY_ZERO,"
                            "NO_AUTO_CREATE_USER', innodb_strict_mode=1",
        },
        'TEST': {
            'COLLATION': "utf8mb4_general_ci",
            'CHARSET': "utf8mb4",
        },
    },
    'other2': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

DATABASE_ROUTERS = [
    'testapp.routers.NothingOnSQLiteRouter',
]

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin.apps.AdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_mysql',
    'testapp',
]

ROOT_URLCONF = 'urls'
TIME_ZONE = 'UTC'
USE_I18N = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
            ],
        },
    },
]


DJANGO_MYSQL_REWRITE_QUERIES = True
